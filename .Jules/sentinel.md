## 2024-04-18 - Prevent CWE-209 Sensitive Information Exposure
**Vulnerability:** Found multiple instances where FastAPI endpoints were catching generic exceptions and returning their string representation (`detail=str(e)`) in `HTTPException` responses.
**Learning:** This pattern is a CWE-209 (Generation of Error Message Containing Sensitive Information) vulnerability. Exposing internal exception details like stack traces, SQL syntax errors, or internal service states to the client provides attackers with insights into the backend architecture and potential exploitation vectors.
**Prevention:** Always log the full exception securely on the server-side using `logging.error(..., exc_info=True)` for debugging purposes, and return a generic, sanitized message (e.g., "Internal server error") to the client via the HTTP response.

## 2026-04-25 - Prevent External Service Resource Exhaustion (Missing Timeouts)
**Vulnerability:** External HTTP requests (e.g., using `requests.get`) were made without explicit timeouts in `nightscout_service.py`.
**Learning:** Omitting timeouts on network calls to third-party services leaves the application vulnerable to Server-Side Request Forgery (SSRF) resource exhaustion or simple Denial of Service (DoS). If the external service hangs or responds very slowly, backend threads handling these requests will block indefinitely, eventually exhausting thread pools and degrading overall application availability.
**Prevention:** Always enforce strict `timeout` parameters (e.g., `timeout=10`) on all external network calls made via the `requests` library or equivalent HTTP clients.
