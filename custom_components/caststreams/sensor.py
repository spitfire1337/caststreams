import logging
import voluptuous as vol
import requests
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)

__version__ = '0.1.5'

_LOGGER = logging.getLogger(__name__)

SYSFILE = '/sys/devices/platform/soc/soc:firmware/get_throttled'

CONF_EMAIL = 'email'
CONF_PASSWORD = 'password'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
    })

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    import os
    email = config.get(CONF_EMAIL)
    password = config.get(CONF_PASSWORD)

    exist = os.path.isfile(SYSFILE)
    if exist:
        add_devices([RaspberryChargerSensor(email, password)], True)
    else:
        _LOGGER.critical('Cant find the system class needed for this component, make sure that your kernel is recent and the hardware is supported.')

class RaspberryChargerSensor(Entity):
    """The class for this sensor"""
    def __init__(self, email, password):
        self._state = None
        self._description = None
        self._email = email
        self._password = password
        self.update()

    def update(self):
        """The update method"""
        # _throttled = open(SYSFILE, 'r').read()[:-1]
        # _throttled = _throttled[:4]
        # if _throttled == '0':
        #     self._description = 'Everything is working as intended'
        # elif _throttled == '1000':
        #     self._description = 'Under-voltage was detected, consider getting a uninterruptible power supply for your Raspberry Pi.'
        # elif _throttled == '2000':
        #     self._description = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        # elif _throttled == '3000':
        #     self._description = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        # elif _throttled == '4000':
        #     self._description = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        # elif _throttled == '5000':
        #     self._description = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        # elif _throttled == '8000':
        #     self._description = 'Your Raspberry Pi is overheating, consider getting a fan or heat sinks.'
        # else:
        #     self._description = 'There is a problem with your power supply or system.'

        r = requests.post('http://api.caststreams.com:2095/login-web', json={"email": "skatermike21988@yahoo.com","androidId":"00:00","deviceId":"02:00:00:00:00:00","password":"skater2","ipaddress":"104.136.250.205"})
        r.status_code
        if r.status_code==200:

            data = r.json()
            #print(data["token"])


            token = data["token"]
            r = requests.get('http://api.caststreams.com:2095/feeds', headers={ "Authorization": token})
            r.status_code
            if r.status_code==200:
                # print(r.text)
                self._state = token
                self._attribute = {'description': "Retrieved stream list"}
            else:
                self._state = "Unavailable"
                self._attribute = {'description': "Failed to retrieve stream list"}
        else:
            # print("Failed")
            self._state = "Unavailable"
            self._attribute = {'description': "Failed to login"}

    @property
    def name(self):
        """Return the name of the sensor"""
        return 'NHL Game Stream'

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return 'mdi:hockey-sticks'

    @property
    def device_state_attributes(self):
        """Return the attribute(s) of the sensor"""
        return self._attribute