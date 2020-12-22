import logging, errno
from socket import error as SocketError

from lmdirect.msgs import Msg, MSGS
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from lmdirect import LMDirect
from lmdirect.const import *

from .const import CONF_CLIENT_ID, CONF_CLIENT_SECRET

_LOGGER = logging.getLogger(__name__)


class LaMarzocco(LMDirect):
    """Keep data for La Marzocco entities."""

    def __init__(self, hass, config):
        """Initialise the weather entity data."""
        self.hass = hass

        super().__init__(
            {
                IP_ADDR: config[CONF_HOST],
                CLIENT_ID: config[CONF_CLIENT_ID],
                CLIENT_SECRET: config[CONF_CLIENT_SECRET],
                USERNAME: config[CONF_USERNAME],
                PASSWORD: config[CONF_PASSWORD],
            }
        )

    async def init_data(self):
        """Init data"""

    async def fetch_data(self):
        """Fetch data from API - (current weather and forecast)."""
        _LOGGER.debug("Fetching data")
        try:
            """Request latest status"""
            await self.request_status()
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise
            else:
                _LOGGER.debug("Connection error: {}".format(e))

        return self

    async def power(self, power):
        """Send power on or power off commands"""
        await self.send_msg(
            Msg.POWER, Msg.POWER_ON_DATA if power else Msg.POWER_OFF_DATA
        )
