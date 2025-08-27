# Nameday API by Valec

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-blue)](https://hacs.xyz/)

**Nameday API by Valec** is a Home Assistant custom integration that provides namedays for today and tomorrow based on your selected country and timezone. It uses the [Nameday API](https://github.com/xnekv03/nameday-api) to fetch data.

---

## Features

- Fetch **today's nameday** and **tomorrow's nameday**.
- User-selectable **country** and **timezone**.
- Automatic daily refresh at **00:01 local time**.
- Supports multiple countries as returned by the Nameday API.
- Lightweight, uses `DataUpdateCoordinator` for efficient updates.

---

## Installation

### HACS

1. Add this repository as a **custom repository** in HACS:
   - Type: Integration
   - URL: `https://github.com/Valecek41/ha-nameday-api-by-valec`
2. Install the integration via HACS.
3. Restart Home Assistant.

### Manual

1. Copy the folder `nameday_api_valec` into `config/custom_components/`.
2. Restart Home Assistant.

---

## Configuration

1. Go to **Settings → Devices & Services → Add Integration → Nameday API by Valec**.
2. Enter your:
   - **Country code** (e.g., `cz`, `de`, `us`, etc.)
   - **Timezone** (e.g., `Europe/Prague`, `Europe/Berlin`)
3. Save.

The integration will create two sensors:

- `sensor.nameday_today` → Today’s nameday.
- `sensor.nameday_tomorrow` → Tomorrow’s nameday.

---

## Example `configuration.yaml` (optional)

> UI configuration is recommended. Only needed if you prefer YAML:

```yaml
nameday_api_valec:
  country: cz
  timezone: Europe/Prague
