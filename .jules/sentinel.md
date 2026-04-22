## 2024-05-01 - SSRF in Nightscout API integrations
**Vulnerability:** The application was vulnerable to Server-Side Request Forgery (SSRF) because it accepted user-provided URLs for connecting to a Nightscout instance and directly fetched data from them using `requests.get()` without first validating the target.
**Learning:** Even internal endpoints that exist to connect to external systems must strictly validate hostnames and IP blocks (checking for private/loopback/link-local) to prevent malicious actors from pivoting into internal infrastructure.
**Prevention:** Implement a central URL validation mechanism that parses the URL, resolves the hostname to an IP address, and asserts that it's not a private or reserved IP, before passing the URL to any request library.
