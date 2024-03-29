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
CONF_TEAM = 'team'
CONF_TYPE = 'usertype'
CONF_REGION = 'region'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_TYPE): cv.string,
    vol.Required(CONF_TEAM): cv.string,
    vol.Optional(CONF_REGION, default="US"): cv.string
    })

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    import os
    email = config.get(CONF_EMAIL)
    password = config.get(CONF_PASSWORD)
    team = config.get(CONF_TEAM)
    usertype = config.get(CONF_TYPE)
    region = config.get(CONF_REGION)
    add_devices([CastStreamsSensor(email, password,team,usertype,region)], True)

class CastStreamsSensor(Entity):
    """The class for this sensor"""
    def __init__(self, email, password,team,usertype,region):
        self._state = None
        self._description = None
        self._email = email
        self._password = password
        self._team = team
        self._auth = None
        self._streamurl = None
        self._usertype = usertype
        self._region = region
        self.update()

    def update(self):
        """The update method"""
        if self._auth == None:
            self.signIn()
        else:
            r = requests.get('http://api.caststreams.com:2095/feeds', headers={ "Authorization": self._auth})
            r.status_code
            if r.status_code==200:
                # print(r.text)
                data = r.json()
                feeds = data["feeds"]

                myteam = False
                dummytext = None
                for feed in feeds:
                    if self._team == feed["away"]["shortName"]:
                        myteam=True
                        url=feed["url"][0].split('-')
                        gamenum=url[0]
                        #self._streamurl=feed["url"][0]
                        if self._usertype=="donor":
                            if self._region=="EU":
                                self._streamurl=gamenum+"-he720"
                            else:
                                self._streamurl=gamenum+"-a720"
                        else:
                            self._streamurl=gamenum+"-a"
                        self._attribute = {'game': feed["name"],'castreams_game': self._streamurl,'status': "Retrieved stream list"}
                        self.getVidLink()
                        break
                    if self._team == feed["home"]["shortName"]:
                        myteam=True
                        url=feed["url"][0].split('-')
                        gamenum=url[0]
                        #self._streamurl=feed["url"][0]
                        if self._usertype=="donor":
                            if self._region=="EU":
                                self._streamurl=gamenum+"-he720"
                            else:
                                self._streamurl=gamenum+"-h720"
                        else:
                            self._streamurl=gamenum+"-a"
                        self._attribute = {'game': feed["name"],'castreams_game': self._streamurl,'status': "Retrieved stream list"}
                        self.getVidLink()
                        break
                    

                #No game today
                if myteam==False:
                    self._state="https://www.caststreams.com/sry/sry.m3u8"
                    self._attribute = {'status': "No game stream available"}



            else:
                self._state = "Unavailable"
                self._attribute = {'status': "Failed to retrieve stream list"}
                self._attribute = {'game': "none"}
                self._auth = None
                self.signIn()

    def getVidLink(self):
        r = requests.get('https://www.caststreams.com/api/getGame?isjson=yes&rUrl='+ self._streamurl, headers={ "Authorization": self._auth})
        r.status_code
        if r.status_code==200:
            data = r.json()
            link=data["link"]
            self._state = link
        else:
            self._state = "Unavailable"
            self._attribute = {'status': "Failed to retrieve stream link"}

    def signIn(self):
        ip = requests.get('https://api.ipify.org').text
        r = requests.post('http://api.caststreams.com:2095/login-web', json={"email": self._email,"androidId":"00:00","deviceId":"02:00:00:00:00:00","password":self._password,"ipaddress":ip})
        r.status_code
        if r.status_code==200:
            data = r.json()
            token = data["token"]
            self._auth = token
            self._attribute = {'loggedin': "True"}
            self.update()
        else:
            self._state = "Unavailable"
            self._attribute = {'description': "Failed to login","ip":ip}
            _LOGGER.error("Couldn't authenticate using the provided credentials!")


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