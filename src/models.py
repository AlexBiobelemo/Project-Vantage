from dataclasses import dataclass


@dataclass
class VPNNode:
    """A data class representing a single VPN node."""

    id: str
    name: str
    country: str
    latency_ms: int
    ip_address: str
