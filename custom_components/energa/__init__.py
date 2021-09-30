"""The Mój Licznik integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .energa import Client
from .const import DOMAIN, DATA_CLIENT, DATA_COORDINATOR

# For your initial PR, limit it to 1 platform.
PLATFORMS: list[str] = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mój Licznik from a config entry."""

    client = Client()

    async def async_update_data():
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
              authenticated = await client.authenticate(hass, entry.data["email"], entry.data["password"], entry.data["token"])
              if authenticated:
                _LOGGER.warning("Energa: authenticated")
                return await client.values()
        except Exception as err:
            _LOGGER.warning(err)
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="energa-sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=3600),
    )
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    await coordinator.async_config_entry_first_refresh()
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    _LOGGER.warning(str(coordinator.data))
    #async_add_entities(EnergaEntity(coordinator, client) for idx, ent in enumerate(coordinator.data))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class EnergaEntity(CoordinatorEntity):

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        client: Client,
    ) -> None:
        """Initialize the Energa entity."""
        super().__init__(coordinator)
        self._client = client


class EnergaDeviceEntity(EnergaEntity):

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Energa instance."""
        return {
            "identifiers": {(DOMAIN)},
            "manufacturer": "Energa",
            "name": "energa",
            "entry_type": "service",
        }
