from __future__ import annotations

import socket


def collect_local_ipv4_addresses() -> set[str]:
    addresses = {"127.0.0.1", "localhost"}
    try:
        hostname = socket.gethostname()
        addresses.add(hostname.lower())
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            addresses.add(info[4][0].lower())
    except OSError:
        pass

    try:
        for info in socket.getaddrinfo(None, 0, socket.AF_INET, socket.SOCK_DGRAM):
            addresses.add(info[4][0].lower())
    except OSError:
        pass

    return addresses


def resolve_firebird_host(host: str | None) -> str:
    """
    Quando a API roda na mesma maquina do Firebird, preferir localhost em vez do IP
    da LAN — evita falhas intermitentes de "Unable to complete network request".
    """
    configured = (host or "").strip()
    if not configured:
        return "localhost"

    lowered = configured.lower()
    if lowered in {"localhost", "127.0.0.1", "::1"}:
        return "localhost"

    if lowered in collect_local_ipv4_addresses():
        return "localhost"

    return configured
