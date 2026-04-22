import socket
import ipaddress
from urllib.parse import urlparse
import logging

class SSRFVulnerabilityError(ValueError):
    pass

def validate_url_for_ssrf(url: str) -> None:
    """
    Validates a URL to prevent Server-Side Request Forgery (SSRF) vulnerabilities.
    Ensures the scheme is http/https and the resolved IP is not private, loopback, etc.
    """
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise SSRFVulnerabilityError("Invalid URL format") from e

    if parsed.scheme not in ("http", "https"):
        raise SSRFVulnerabilityError(f"Invalid scheme: {parsed.scheme}. Only http and https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise SSRFVulnerabilityError("No hostname found in URL")

    try:
        ip_addr = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        raise SSRFVulnerabilityError(f"Could not resolve hostname: {hostname}") from e

    ip = ipaddress.ip_address(ip_addr)

    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
        raise SSRFVulnerabilityError(f"URL resolves to a non-public IP address: {ip_addr}")
