## Scripts

### Check Home Assistant on LAN

`check_home_assistant_lan.py` discovers Home Assistant on your LAN and verifies it is reachable and serving the HA frontend.

Examples:

- CCA configuration (per-project defaults):

```bash
python3 scripts/check_home_assistant_lan.py --config cca
```

This checks:
- HA at `192.168.8.248:8123` and also via `homeassistant.local` / `homeassistantcca.local`
- Router/hub admin reachability at `192.168.8.1` (ports 80/443)

- Check via mDNS (common defaults like `homeassistant.local`):

```bash
python3 scripts/check_home_assistant_lan.py
```

- Check a specific host/IP:

```bash
python3 scripts/check_home_assistant_lan.py --host 192.168.1.50
python3 scripts/check_home_assistant_lan.py --host homeassistant.local
```

- Scan a subnet for port 8123 then verify HA:

```bash
python3 scripts/check_home_assistant_lan.py --cidr 192.168.1.0/24
```

Exit codes:
- `0`: found and healthy
- `2`: not found / not reachable
- `3`: reachable but did not look like Home Assistant

