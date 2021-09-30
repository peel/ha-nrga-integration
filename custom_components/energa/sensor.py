"""Support for OVO Energy sensors."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Callable, Final

from homeassistant.components.sensor import (
    STATE_CLASS_TOTAL_INCREASING,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_MONETARY,
    DEVICE_CLASS_TIMESTAMP,
    ENERGY_KILO_WATT_HOUR,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from . import EnergaDeviceEntity
from .energa import Client
from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN

SCAN_INTERVAL = timedelta(seconds=300)
PARALLEL_UPDATES = 4

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]
    client: Client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    entities = []
    print(coordinator.data)
    if coordinator.data:
       entities = list(map(lambda metric: EnergaSensor(coordinator, metric["zone"], client), coordinator.data))
    async_add_entities(entities, True)

class EnergaSensor(EnergaDeviceEntity, SensorEntity):
    """Define a Energa sensor."""

    coordinator: DataUpdateCoordinator
    device_class = DEVICE_CLASS_ENERGY
    state_class = STATE_CLASS_TOTAL_INCREASING
    native_unit_of_measurement = ENERGY_KILO_WATT_HOUR


    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        measurement_name: str,
        client: Client,
    ) -> None:
        """Initialize."""
        super().__init__(
            coordinator,
            client,
        )
        self._attr_unique_id = f"{DOMAIN}_{measurement_name}"
        self.measurement_name = measurement_name

    @property
    def native_value(self) -> StateType:
        """Return the state."""
        return next(filter(lambda x: x['zone'] == self.measurement_name, self.coordinator.data))['value']
