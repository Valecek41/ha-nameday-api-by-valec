from datetime import datetime, timedelta
import logging
import async_timeout
import requests
import pytz
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_COUNTRY, CONF_TIMEZONE

_LOGGER = logging.getLogger(__name__)

# Map standard timezone strings to Nameday API city names
TIMEZONE_CITY_MAP = {
    "Europe/Prague": "Prague",
    "Europe/Paris": "Paris",
    "Europe/Berlin": "Berlin",
    "Europe/Rome": "Rome",
    "Europe/London": "London",
    "Europe/Warsaw": "Warsaw",
    "Europe/Vienna": "Vienna",
    "Europe/Budapest": "Budapest",
    # Add more as needed
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    country = entry.data[CONF_COUNTRY]
    timezone = entry.data[CONF_TIMEZONE]

    city = TIMEZONE_CITY_MAP.get(timezone, timezone)

    async def async_update_data():
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        # URLs
        url_today = f"https://nameday.abalin.net/api/V2/today/{city}"
        tomorrow = now + timedelta(days=1)
        url_tomorrow = f"https://nameday.abalin.net/api/V2/date?day={tomorrow.day}&month={tomorrow.month}"

        try:
            async with async_timeout.timeout(10):
                # Fetch today
                response_today = await hass.async_add_executor_job(requests.get, url_today)
                response_today.raise_for_status()
                data_today = response_today.json().get("data", {})
                nameday_today = data_today.get(country)
                if not nameday_today or nameday_today.lower() == "n/a":
                    nameday_today = "Unavailable"

                # Fetch tomorrow
                response_tomorrow = await hass.async_add_executor_job(requests.get, url_tomorrow)
                response_tomorrow.raise_for_status()
                data_tomorrow = response_tomorrow.json().get("data", {})
                nameday_tomorrow = data_tomorrow.get(country)
                if not nameday_tomorrow or nameday_tomorrow.lower() == "n/a":
                    nameday_tomorrow = "Unavailable"

                _LOGGER.debug("Nameday today: %s, tomorrow: %s", nameday_today, nameday_tomorrow)

                return {
                    "today": nameday_today,
                    "tomorrow": nameday_tomorrow
                }

        except Exception as err:
            raise UpdateFailed(f"Error fetching nameday: {err}")

    # Coordinator refresh interval is initially arbitrary
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="nameday",
        update_method=async_update_data,
        update_interval=timedelta(hours=12),  # dummy initial value
    )

    # First refresh immediately
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Forward setup to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )

    # Schedule daily refresh at 00:01 local time
    async def daily_reschedule():
        tz = pytz.timezone(timezone)
        while True:
            now_local = datetime.now(tz)
            next_run = datetime.combine(now_local.date() + timedelta(days=1), datetime.min.time()) + timedelta(minutes=1)
            seconds_until_next_run = (next_run - now_local).total_seconds()
            await asyncio.sleep(seconds_until_next_run)
            await coordinator.async_request_refresh()

    hass.async_create_task(daily_reschedule())

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
