import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { GoogleAuth } from 'google-auth-library';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 8080;

// Configuration
const BACKEND_URL = process.env.BACKEND_URL;
const FIREBASE_PROJECT_ID = process.env.VITE_FIREBASE_PROJECT_ID;

if (!BACKEND_URL) {
    console.error('Error: BACKEND_URL environment variable is not set.');
    process.exit(1);
}

console.log(`Starting BFF server...`);
console.log(`Backend URL: ${BACKEND_URL}`);
if (FIREBASE_PROJECT_ID) {
    console.log(`Firebase Project ID: ${FIREBASE_PROJECT_ID}`);
} else {
    console.warn('Warning: VITE_FIREBASE_PROJECT_ID environment variable is not set. Auth proxy will not be configured.');
}

const FIREBASE_AUTH_DOMAIN = process.env.VITE_FIREBASE_AUTH_DOMAIN || 'ns-ai-project.firebaseapp.com';
console.log(`Firebase Auth Domain: ${FIREBASE_AUTH_DOMAIN}`);

// Initialize Google Auth Client
const auth = new GoogleAuth();

// Function to get ID token
async function getIdToken(audience) {
    try {
        const client = await auth.getIdTokenClient(audience);
        const headers = await client.getRequestHeaders();
        return headers['Authorization'].split(' ')[1];
    } catch (error) {
        console.error('Error fetching ID token:', error);
        return null;
    }
}

// Proxy middleware for API requests
const apiProxy = createProxyMiddleware({
    target: BACKEND_URL,
    changeOrigin: true,
    pathRewrite: {
        '^/api': '', // Remove /api prefix when forwarding to backend
    },
    onProxyReq: async (proxyReq, req, res) => {
        console.log(`Proxying request: ${req.method} ${req.path} -> ${BACKEND_URL}`);

        // Add OIDC token to Authorization header
        const token = await getIdToken(BACKEND_URL);
        if (token) {
            proxyReq.setHeader('Authorization', `Bearer ${token}`);
        } else {
            console.warn('Failed to obtain ID token, sending request without Authorization header.');
        }
    },
    onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).send('Proxy error');
    }
});

// Proxy middleware for Firebase Auth
if (FIREBASE_PROJECT_ID) {
    const authProxy = createProxyMiddleware({
        target: `https://${FIREBASE_PROJECT_ID}.firebaseapp.com`,
        changeOrigin: true,
        secure: true,
    });
    app.use('/__/auth', authProxy);
}

// Use proxy for /api routes
app.use('/api', apiProxy);

// Proxy for Firebase Auth routes (needed for custom domains)
const authProxy = createProxyMiddleware({
    target: `https://${FIREBASE_AUTH_DOMAIN}`,
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        console.log(`Proxying Auth request: ${req.method} ${req.path} -> https://${FIREBASE_AUTH_DOMAIN}`);
    },
    onError: (err, req, res) => {
        console.error('Auth Proxy error:', err);
        res.status(500).send('Auth Proxy error');
    }
});

app.use('/__/auth', authProxy);

// Serve static files from the 'dist' directory (Vite build output)
app.use(express.static(path.join(__dirname, 'dist')));

// Handle client-side routing: return index.html for all non-API requests
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
    console.log(`BFF server listening on port ${port}`);
});
