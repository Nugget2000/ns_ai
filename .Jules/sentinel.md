## 2024-04-18 - Prevent CWE-209 Sensitive Information Exposure
**Vulnerability:** Found multiple instances where FastAPI endpoints were catching generic exceptions and returning their string representation (`detail=str(e)`) in `HTTPException` responses.
**Learning:** This pattern is a CWE-209 (Generation of Error Message Containing Sensitive Information) vulnerability. Exposing internal exception details like stack traces, SQL syntax errors, or internal service states to the client provides attackers with insights into the backend architecture and potential exploitation vectors.
**Prevention:** Always log the full exception securely on the server-side using `logging.error(..., exc_info=True)` for debugging purposes, and return a generic, sanitized message (e.g., "Internal server error") to the client via the HTTP response.

## 2026-04-18 - Additional CWE-209 Information Exposure Vectors
**Vulnerability:** Found multiple instances where internal error messages (`str(e)`) were leaked to the client outside of standard HTTP endpoints, such as in WebSockets/Streaming generators (Emanuel service), internal API connection tests (Nightscout service), and authentication layers.
**Learning:** The CWE-209 vulnerability pattern is not limited to standard HTTP endpoint error responses. Any interface that returns data to the client, including streaming chunks, error dictionaries from internal test functions, and authentication exceptions, must be sanitized.
**Prevention:** Apply the principle of returning generic error messages while logging the full exception internally to all communication layers and service responses, not just top-level API routes.
