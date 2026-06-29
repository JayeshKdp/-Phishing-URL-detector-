"""URL feature extraction utilities for the phishing detector."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import parse_qs, urlparse


SUSPICIOUS_KEYWORDS = (
    "login",
    "verify",
    "account",
    "secure",
    "bank",
    "update",
    "signin",
    "paypal",
    "password",
    "confirm",
    "billing",
    "wallet",
    "support",
    "recover",
    "limited",
)

FEATURE_NAMES = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_at_symbols",
    "num_digits",
    "num_special_chars",
    "has_https",
    "has_ip_address",
    "num_subdomains",
    "suspicious_keyword_count",
    "num_slashes",
    "has_query_params",
]


def normalize_url(url: str) -> str:
    """Return a URL with a scheme so urlparse can read the hostname."""
    cleaned = (url or "").strip()
    if not cleaned:
        return ""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", cleaned):
        cleaned = f"http://{cleaned}"
    return cleaned


def is_valid_url(url: str) -> bool:
    """Validate that a user supplied URL has a host-like network location."""
    normalized = normalize_url(url)
    if not normalized:
        return False

    parsed = urlparse(normalized)
    host = parsed.hostname
    if not host or " " in host:
        return False

    if "." not in host and host.lower() != "localhost":
        return False

    return True


def _host_has_ip(host: str) -> int:
    host = (host or "").strip("[]")
    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0


def _subdomain_count(host: str) -> int:
    if not host or _host_has_ip(host):
        return 0

    labels = [part for part in host.split(".") if part]
    if len(labels) <= 2:
        return 0

    common_second_level_tlds = {"co", "com", "net", "org", "gov", "ac"}
    if len(labels) > 3 and labels[-2] in common_second_level_tlds and len(labels[-1]) == 2:
        return max(len(labels) - 3, 0)

    return max(len(labels) - 2, 0)


def extract_features(url: str) -> dict[str, int]:
    """Extract deterministic URL-only features used by the ML model."""
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    host = parsed.hostname or ""
    lowered = normalized.lower()
    query_params = parse_qs(parsed.query, keep_blank_values=True)

    special_chars = sum(1 for char in normalized if not char.isalnum())

    return {
        "url_length": len(normalized),
        "num_dots": normalized.count("."),
        "num_hyphens": normalized.count("-"),
        "num_at_symbols": normalized.count("@"),
        "num_digits": sum(char.isdigit() for char in normalized),
        "num_special_chars": special_chars,
        "has_https": 1 if parsed.scheme.lower() == "https" else 0,
        "has_ip_address": _host_has_ip(host),
        "num_subdomains": _subdomain_count(host),
        "suspicious_keyword_count": sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in lowered),
        "num_slashes": normalized.count("/"),
        "has_query_params": 1 if query_params else 0,
    }


def features_as_list(url: str) -> list[int]:
    features = extract_features(url)
    return [features[name] for name in FEATURE_NAMES]
