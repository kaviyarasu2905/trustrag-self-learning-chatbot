"""
TrustRAG - Verifier Agent Module
"""

from .verifier_agent import (
    compute_confidence,
    route_query,
    verify_and_route,
    DEFAULT_CONFIDENCE_THRESHOLD,
    HIGH_CONFIDENCE_THRESHOLD,
    LOW_CONFIDENCE_THRESHOLD,
)

__all__ = [
    "compute_confidence",
    "route_query",
    "verify_and_route",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "HIGH_CONFIDENCE_THRESHOLD",
    "LOW_CONFIDENCE_THRESHOLD",
]
