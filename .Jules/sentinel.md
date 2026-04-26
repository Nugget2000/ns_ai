## 2024-04-18 - Prevent CWE-209 Sensitive Information Exposure
**Vulnerability:** Found multiple instances where FastAPI endpoints were catching generic exceptions and returning their string representation (`detail=str(e)`) in `HTTPException` responses.
**Learning:** This pattern is a CWE-209 (Generation of Error Message Containing Sensitive Information) vulnerability. Exposing internal exception details like stack traces, SQL syntax errors, or internal service states to the client provides attackers with insights into the backend architecture and potential exploitation vectors.
**Prevention:** Always log the full exception securely on the server-side using `logging.error(..., exc_info=True)` for debugging purposes, and return a generic, sanitized message (e.g., "Internal server error") to the client via the HTTP response.

## 2024-04-26 - Prevent Overly Permissive CORS Headers
**Vulnerability:** Found `allow_headers=["*"]` combined with `allow_credentials=True` in FastAPI `CORSMiddleware` configuration.
**Learning:** Using a wildcard for `allow_headers` when `allow_credentials=True` is enabled can lead to security misconfigurations. If an application requires credentials (like cookies or Authorization headers), allowing any request header can expose the application to unintended cross-origin requests that might exploit custom headers, potentially leading to unauthorized data access or actions.
**Prevention:** Always explicitly define the allowed headers (e.g., `allow_headers=["Content-Type", "Authorization"]`) in the CORS configuration when `allow_credentials=True` is set, rather than using a wildcard.
