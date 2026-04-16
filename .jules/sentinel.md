## 2026-04-16 - [Information Exposure Through Error Messages (CWE-209)]
**Vulnerability:** API endpoints were using `raise HTTPException(status_code=500, detail=str(e))`, which returns the stringified exception directly to the client.
**Learning:** This leaks internal state, potentially exposing sensitive stack traces, paths, or data to unauthorized users.
**Prevention:** Catch exceptions, log them securely internally using `logging.error(..., exc_info=True)`, and return a generic 'Internal server error' in the `HTTPException` detail parameter.
