from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_COUNTRY, CONF_TIMEZONE

class NamedayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"Nameday API by Valec ({user_input[CONF_COUNTRY]})",
                data=user_input
            )

        data_schema = vol.Schema({
            vol.Required(CONF_TIMEZONE): str,
            vol.Required(CONF_COUNTRY): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)