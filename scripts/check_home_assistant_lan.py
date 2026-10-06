#!/usr/bin/env python3
"""
Check for Home Assistant on the LAN and verify it's up.

Discovery:
  - By default, tries common mDNS hostnames (e.g. homeassistant.local).
  - Optionally scans a CIDR (e.g. 192.168.1.0/24) for port 8123.

Health check:
  - HTTP GET to http://<host>:8123/ (or --https) with a short timeout.
  - Looks for typical Home Assistant markers in the response.

Exit codes:
  0 = found and healthy
  2 = not found / not reachable
  3 = reachable but did not look like Home Assistant / unhealthy
"""

from __future__ import annotations

import argparse
import ipaddress
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence


DEFAULT_MDNS_HOSTS = (
    "homeassistant.local",
    "home-assistant.local",
    "hass.local",
    "hassio.local",
)

CONFIGS = {
    # Note: only CCA is fully specified by requirements; others are kept generic but overrideable.
    "home": {
        "ha_hosts": list(DEFAULT_MDNS_HOSTS),
        "ha_ip": None,
        "router_ip": None,
        "router_admin_url": None,
    },
    "cca": {
        "ha_hosts": ["homeassistant.local", "homeassistantcca.local"],
        "ha_ip": "192.168.8.248",
        "router_ip": "192.168.8.1",
        "router_admin_url": "http://192.168.8.1/",
    },
    "alt": {
        "ha_hosts": list(DEFAULT_MDNS_HOSTS),
        "ha_ip": None,
        "router_ip": None,
        "router_admin_url": None,
    },
}


@dataclass(frozen=True)
class Candidate:
    host: str
    ip: Optional[str] = None


def resolve_host(host: str, timeout_s: float) -> Optional[str]:
    # DNS/mDNS resolution timeout is OS-dependent; mitigate by using a thread.
    result: dict[str, Optional[str]] = {"ip": None}

    def _work() -> None:
        try:
            result["ip"] = socket.gethostbyname(host)
        except OSError:
            result["ip"] = None

    t = threading.Thread(target=_work, daemon=True)
    t.start()
    t.join(timeout=timeout_s)
    return result["ip"]


def tcp_port_open(ip: str, port: int, timeout_s: float) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def pick_first_open_port(ip: str, ports: Sequence[int], timeout_s: float) -> Optional[int]:
    for port in ports:
        if tcp_port_open(ip, port, timeout_s):
            return port
    return None


def http_looks_like_home_assistant(url: str, timeout_s: float) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "check_home_assistant_lan/1.0",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = getattr(resp, "status", 0)
            body = resp.read(256 * 1024)  # cap read
            text = body.decode("utf-8", errors="ignore")
            hay = (text + "\n" + "\n".join(f"{k}: {v}" for k, v in resp.headers.items())).lower()

            # Heuristics: HA's frontend HTML includes these markers.
            markers = (
                "home assistant",
                "frontend_latest",
                "manifest.json",
                "ha-version",
                "supervisor",
            )
            ok = status in (200, 301, 302) and any(m in hay for m in markers)
            return ok, f"http_status={status}"
    except urllib.error.HTTPError as e:
        # Some setups redirect/require auth, but if we get a response with HA-ish headers/body, accept.
        try:
            body = e.read(128 * 1024)
            text = body.decode("utf-8", errors="ignore").lower()
            hdrs = "\n".join(f"{k}: {v}" for k, v in e.headers.items()).lower()
            hay = text + "\n" + hdrs
            markers = ("home assistant", "ha-version", "frontend_latest", "manifest.json")
            ok = any(m in hay for m in markers)
            return ok, f"http_error={e.code}"
        except (OSError, ValueError, UnicodeError):
            return False, f"http_error={e.code}"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return False, f"http_error={type(e).__name__}"


def iter_cidr_hosts(cidr: str) -> Iterable[str]:
    net = ipaddress.ip_network(cidr, strict=False)
    # Avoid huge scans by default: caller can still pass /16, but it will be slow.
    for ip in net.hosts():
        yield str(ip)


def scan_cidr_for_port(
    cidr: str,
    port: int,
    timeout_s: float,
    concurrency: int,
    deadline_s: float,
) -> Optional[str]:
    lock = threading.Lock()
    found: dict[str, Optional[str]] = {"ip": None}
    start = time.time()

    ips = iter_cidr_hosts(cidr)

    def worker() -> None:
        nonlocal ips
        while True:
            if time.time() - start > deadline_s:
                return
            with lock:
                if found["ip"] is not None:
                    return
                try:
                    ip = next(ips)
                except StopIteration:
                    return
            if tcp_port_open(ip, port, timeout_s):
                with lock:
                    if found["ip"] is None:
                        found["ip"] = ip
                return

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, concurrency))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return found["ip"]


def main() -> int:
    p = argparse.ArgumentParser(description="Discover Home Assistant on LAN and verify it's up.")
    p.add_argument("--config", choices=sorted(CONFIGS.keys()), help="Use a named config (home, cca, alt).")
    p.add_argument("--host", help="Hostname or IP to check directly (skips discovery).")
    p.add_argument("--ha-host", action="append", help="Additional HA hostname to try (repeatable).")
    p.add_argument("--ha-ip", help="HA IP to try directly (in addition to hostnames).")
    p.add_argument("--mdns", action="store_true", help="Try common mDNS hostnames (default if no --host/--cidr).")
    p.add_argument("--cidr", help="CIDR to scan for port 8123 (e.g. 192.168.1.0/24).")
    p.add_argument("--port", type=int, default=8123, help="Home Assistant port (default: 8123).")
    p.add_argument("--https", action="store_true", help="Use https:// instead of http:// for the health check.")
    p.add_argument("--router-ip", help="Router/hub IP to verify is reachable.")
    p.add_argument(
        "--router-ports",
        default="80,443",
        help="Comma-separated router ports to consider reachable (default: 80,443).",
    )
    p.add_argument("--timeout", type=float, default=1.5, help="Per-step timeout in seconds (default: 1.5).")
    p.add_argument("--resolve-timeout", type=float, default=1.0, help="Hostname resolve timeout in seconds (default: 1.0).")
    p.add_argument("--scan-concurrency", type=int, default=64, help="CIDR scan concurrency (default: 64).")
    p.add_argument("--scan-deadline", type=float, default=25.0, help="Max seconds to spend scanning CIDR (default: 25).")
    p.add_argument("--quiet", action="store_true", help="Only exit code; print nothing.")
    args = p.parse_args()

    scheme = "https" if args.https else "http"

    cfg = CONFIGS.get(args.config) if args.config else None

    # Router reachability check (optional but required for CCA config).
    router_ip = args.router_ip or (cfg["router_ip"] if cfg else None)
    router_ports: list[int] = []
    try:
        router_ports = [int(p.strip()) for p in str(args.router_ports).split(",") if p.strip()]
    except ValueError:
        router_ports = [80, 443]

    if router_ip:
        open_port = pick_first_open_port(router_ip, router_ports, args.timeout)
        if open_port is None:
            if not args.quiet:
                print(f"ROUTER_DOWN: {router_ip} not reachable on ports {router_ports}", file=sys.stderr)
            return 2
        if not args.quiet:
            print(f"ROUTER_OK: {router_ip} port={open_port}")

    candidates: list[Candidate] = []

    if args.host:
        ip = None
        try:
            ipaddress.ip_address(args.host)
            ip = args.host
        except ValueError:
            ip = resolve_host(args.host, args.resolve_timeout)
        candidates.append(Candidate(host=args.host, ip=ip))
    else:
        # Config-provided direct IP (if any)
        ha_ip = args.ha_ip or (cfg["ha_ip"] if cfg else None)
        if ha_ip:
            candidates.append(Candidate(host=ha_ip, ip=ha_ip))

        if args.cidr:
            ip = scan_cidr_for_port(
                args.cidr,
                port=args.port,
                timeout_s=args.timeout,
                concurrency=args.scan_concurrency,
                deadline_s=args.scan_deadline,
            )
            if ip:
                candidates.append(Candidate(host=ip, ip=ip))

        config_hosts: list[str] = []
        if cfg:
            config_hosts.extend(list(cfg["ha_hosts"]))
        if args.ha_host:
            config_hosts.extend(args.ha_host)

        if args.mdns or (not args.cidr and not config_hosts):
            config_hosts.extend(list(DEFAULT_MDNS_HOSTS))

        # Keep order but de-dupe
        seen_hosts: set[str] = set()
        ordered_hosts: list[str] = []
        for h in config_hosts:
            if h and h not in seen_hosts:
                ordered_hosts.append(h)
                seen_hosts.add(h)

        for h in ordered_hosts:
                ip = resolve_host(h, args.resolve_timeout)
                if ip:
                    candidates.append(Candidate(host=h, ip=ip))

    # De-dupe by IP/host
    seen: set[tuple[str, Optional[str]]] = set()
    uniq: list[Candidate] = []
    for c in candidates:
        key = (c.host, c.ip)
        if key not in seen:
            uniq.append(c)
            seen.add(key)

    if not uniq:
        if not args.quiet:
            print("NOT_FOUND: no candidates discovered", file=sys.stderr)
        return 2

    for c in uniq:
        ip = c.ip or c.host
        if not ip:
            continue
        if not tcp_port_open(ip, args.port, args.timeout):
            continue
        url = f"{scheme}://{c.host}:{args.port}/"
        ok, detail = http_looks_like_home_assistant(url, args.timeout * 2)
        if ok:
            if not args.quiet:
                shown_ip = f" ({c.ip})" if c.ip and c.ip != c.host else ""
                print(f"HA_OK: {c.host}{shown_ip} {detail}")
            return 0

    # If something had port open but didn't look like HA, return unhealthy.
    # Otherwise, not reachable.
    any_open = any(c.ip and tcp_port_open(c.ip, args.port, args.timeout) for c in uniq)
    if any_open:
        if not args.quiet:
            print("HA_UNHEALTHY: port open but did not look like Home Assistant", file=sys.stderr)
        return 3

    if not args.quiet:
        print("HA_NOT_FOUND: no reachable Home Assistant on port", args.port, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

