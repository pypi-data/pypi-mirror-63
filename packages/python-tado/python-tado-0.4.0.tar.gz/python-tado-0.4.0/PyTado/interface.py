"""
PyTado interface implementation for mytado.com
"""

import logging
import json
import datetime
from requests import Session


from enum import IntEnum


_LOGGER = logging.getLogger(__name__)


class Tado:
    """Interacts with a Tado thermostat via public API.
    Example usage: t = Tado('me@somewhere.com', 'mypasswd')
                   t.getClimate(1) # Get climate, zone 1.
    """

    """Constants needed for get/set Schedule and Timetable"""
    class Timetable(IntEnum):
        ONE_DAY = 0
        THREE_DAY = 1
        SEVEN_DAY = 2

    _debugCalls = False

    # Instance-wide constant info
    headers = {'Referer' : 'https://my.tado.com/'}
    api2url = 'https://my.tado.com/api/v2/homes/'
    mobi2url = 'https://my.tado.com/mobile/1.9/'
    refresh_token = ''
    refresh_at = datetime.datetime.now() + datetime.timedelta(minutes=5)
    timeout = 10

    # 'Private' methods for use in class, Tado mobile API V1.9.
    def _mobile_apiCall(self, cmd):
        # pylint: disable=C0103

        self._refresh_token()

        if self._debugCalls:
            _LOGGER.debug("mobile api: %s",
                          cmd)

        url = '%s%s' % (self.mobi2url, cmd)
        response = self._http_session.request("get", url, headers=self.headers, timeout=self.timeout)

        if self._debugCalls:
            _LOGGER.debug("mobile api: %s, response: %s",
                          cmd, response.text)

        return response.json()

    # 'Private' methods for use in class, Tado API V2.
    def _apiCall(self, cmd, method="GET", data=None, plain=False):
        # pylint: disable=C0103

        self._refresh_token()

        headers = self.headers

        if data is not None:
            if plain:
                headers['Content-Type'] = 'text/plain;charset=UTF-8'
            else:
                headers['Content-Type'] = 'application/json;charset=UTF-8'
            headers['Mime-Type'] = 'application/json;charset=UTF-8'
            data = json.dumps(data).encode('utf8')

        if self._debugCalls:
            _LOGGER.debug("api call: %s: %s, headers %s, data %s", method, cmd, headers, data)

        url = '%s%i/%s' % (self.api2url, self.id, cmd)
        response = self._http_session.request(method, url, timeout=self.timeout,
                                    headers=headers,
                                    data=data)

        if self._debugCalls:
            _LOGGER.debug("api call: %s: %s, response %s",
                          method, cmd, response.text)
        
        str_response = response.text
        if str_response is None or str_response == "":
            return

        return response.json()


    def _setOAuthHeader(self, data):
        # pylint: disable=C0103

        access_token = data['access_token']
        expires_in = float(data['expires_in'])
        refresh_token = data['refresh_token']

        self.refresh_token = refresh_token
        self.refresh_at = datetime.datetime.now()
        self.refresh_at = self.refresh_at + datetime.timedelta(seconds=expires_in)

        # we substract 30 seconds from the correct refresh time
        # then we have a 30 seconds timespan to get a new refresh_token
        self.refresh_at = self.refresh_at + datetime.timedelta(seconds=-30)

        self.headers['Authorization'] = 'Bearer ' + access_token

    def _refresh_token(self):
        if self.refresh_at >= datetime.datetime.now():
            return False

        url = 'https://auth.tado.com/oauth/token'
        data = {'client_id' : 'public-api-preview',
                'client_secret' : '4HJGRffVR8xb3XdEUQpjgZ1VplJi6Xgw',
                'grant_type' : 'refresh_token',
                'scope' : 'home.user',
                'refresh_token' : self.refresh_token}
        # pylint: disable=R0204
        response = self._http_session.request("post", url, params=data, timeout=self.timeout, data=json.dumps({}).encode('utf8'),
                                     headers={'Content-Type': 'application/json',
                                              'Referer' : 'https://my.tado.com/'})

        _LOGGER.info("api call result: %s", response.text)
        self._setOAuthHeader(response.json())

    def _loginV2(self, username, password):
        # pylint: disable=C0103

        headers = self.headers
        headers['Content-Type'] = 'application/json'

        url = 'https://auth.tado.com/oauth/token'
        data = {'client_id' : 'public-api-preview',
                'client_secret' : '4HJGRffVR8xb3XdEUQpjgZ1VplJi6Xgw',
                'grant_type' : 'password',
                'password' : password,
                'scope' : 'home.user',
                'username' : username}
        # pylint: disable=R0204
        response = self._http_session.request("post", url, params=data, timeout=self.timeout, data=json.dumps({}).encode('utf8'),
                                     headers={'Content-Type': 'application/json',
                                              'Referer' : 'https://my.tado.com/'})

        self._setOAuthHeader(response.json())

    def setDebugging(self, debugCalls):
        self._debugCalls = debugCalls
        return self._debugCalls

    # Public interface
    def getMe(self):
        """Gets home information."""
        # pylint: disable=C0103

        url = 'https://my.tado.com/api/v2/me'
        return self._http_session.request("get", url, headers=self.headers, timeout=self.timeout).json()

    def getDevices(self):
        """Gets device information."""
        # pylint: disable=C0103

        cmd = 'devices'
        data = self._apiCall(cmd)
        return data

    def getZones(self):
        """Gets zones information."""
        # pylint: disable=C0103

        cmd = 'zones'
        data = self._apiCall(cmd)
        return data

    def getState(self, zone):
        """Gets current state of Zone zone."""
        # pylint: disable=C0103

        cmd = 'zones/%i/state' % zone
        data = self._apiCall(cmd)
        return data

    def getHomeState(self):
        """Gets current state of Home."""
        # returns {"presence":"AWAY"} or {"presence":"HOME"}
        # without an auto assist skill presence is not switched automatically,
        # but a button is shown in the app. showHomePresenceSwitchButton
        # is an indicator, that the homeState can be switched
        # {"presence":"HOME","showHomePresenceSwitchButton":true}
        cmd = 'state'
        data = self._apiCall(cmd)
        return data
    
    def getCapabilities(self, zone):
        """Gets current capabilities of Zone zone."""
        # pylint: disable=C0103

        cmd = 'zones/%i/capabilities' % zone
        data = self._apiCall(cmd)
        return data

    def getClimate(self, zone):
        """Gets temp (centigrade) and humidity (% RH) for Zone zone."""
        # pylint: disable=C0103

        data = self.getState(zone)['sensorDataPoints']
        return {'temperature' : data['insideTemperature']['celsius'],
                'humidity'    : data['humidity']['percentage']}

    def getTimetable(self, zone):
        """Get the Timetable type currently active"""
        # pylint: disable=C0103

        cmd = 'zones/%i/schedule/activeTimetable' % (zone)

        data = self._apiCall(cmd, "GET", {}, True)

        if "id" in data:
            return Tado.Timetable(data["id"])

        raise Exception('Returned data did not contain "id" : '+str(data))

    def getHistoric(self, zone, date):
        """Gets historic information on given date for Zone zone."""
        try:
            day = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

        cmd = 'zones/%i/dayReport?date=%s' % (zone, day.strftime('%Y-%m-%d'))
        data = self._apiCall(cmd)
        return data

    def setTimetable(self, zone, id):
        """Set the Timetable type currently active
           id = 0 : ONE_DAY (MONDAY_TO_SUNDAY)
           id = 1 : THREE_DAY (MONDAY_TO_FRIDAY, SATURDAY, SUNDAY)
           id = 3 : SEVEN_DAY (MONDAY, TUESDAY, WEDNESDAY ...)"""
        # pylint: disable=C0103

        # Type checking
        if not isinstance(id, Tado.Timetable):
            raise TypeError('id must be an instance of Tado.Timetable')

        cmd = 'zones/%i/schedule/activeTimetable' % (zone)

        data = self._apiCall(cmd, "PUT", {'id': id }, True)
        return data

    def getSchedule(self, zone, id, day=None):
        """Get the JSON representation of the schedule for a zone
           a Zone has 3 different schedules, one for each timetable
           (see setTimetable) """
        # pylint: disable=C0103

        # Type checking
        if not isinstance(id, Tado.Timetable):
            raise TypeError('id must be an instance of Tado.Timetable')

        if day:
            cmd = 'zones/%i/schedule/timetables/%i/blocks/%s' % (zone,id,day)
        else:
            cmd = 'zones/%i/schedule/timetables/%i/blocks' % (zone,id)

        data = self._apiCall(cmd, "GET", {}, True)
        return data


    def setSchedule(self, zone, id, day, data):
        """Set the schedule for a zone, day is required"""
        # pylint: disable=C0103

        # Type checking
        if not isinstance(id, Tado.Timetable):
            raise TypeError('id must be an instance of Tado.Timetable')

        cmd = 'zones/%i/schedule/timetables/%i/blocks/%s' % (zone,id,day)

        data = self._apiCall(cmd, "PUT", data, True)
        return data

    def getWeather(self):
        """Gets outside weather data"""
        # pylint: disable=C0103

        cmd = 'weather'
        data = self._apiCall(cmd)
        return data

    def getAppUsers(self):
        """Gets getAppUsers data"""
        # pylint: disable=C0103

        cmd = 'getAppUsers'
        data = self._mobile_apiCall(cmd)
        return data

    def getAppUsersRelativePositions(self):
        """Gets getAppUsersRelativePositions data"""
        # pylint: disable=C0103

        cmd = 'getAppUsersRelativePositions'
        data = self._mobile_apiCall(cmd)
        return data
    
    def getMobileDevices(self):
        """Gets information about mobile devices"""

        cmd = 'mobileDevices'
        data = self._apiCall(cmd)
        return data
    
    def resetZoneOverlay(self, zone):
        """Delete current overlay"""
        # pylint: disable=C0103

        cmd = 'zones/%i/overlay' % zone
        data = self._apiCall(cmd, "DELETE", {}, True)
        return data

    def setZoneOverlay(self, zone, overlayMode, setTemp=None, duration=None, deviceType='HEATING', power="ON", mode=None, fanSpeed=None):
        """set current overlay for a zone"""
        # pylint: disable=C0103

        cmd = 'zones/%i/overlay' % zone

        post_data = {
            "setting": {"type": deviceType, "power": power},
            "termination": {"type": overlayMode},
        }

        if setTemp is not None:
            post_data["setting"]["temperature"] = {"celsius": setTemp}
            if fanSpeed is not None:
                post_data["setting"]["fanSpeed"] = fanSpeed

        if mode is not None:
            post_data["setting"]["mode"] = mode

        if duration is not None:
            post_data["termination"]["durationInSeconds"] = duration

        data = self._apiCall(cmd, "PUT", post_data)
        return data

    def setHome(self):
        """Sets HomeState to HOME """
        # it seems, this can be set anytime
        cmd = 'presence'
        payload = { "homePresence": "HOME" }
        data = self._apiCall(cmd, "PUT", payload)
        return data

    def setAway(self):
        """Sets HomeState to AWAY """
        # this can only be set if everybody left the home and 
        # showHomePresenceSwitchButton = true
        cmd = 'presence'
        payload = { "homePresence": "AWAY" }
        data = self._apiCall(cmd, "PUT", payload)
        return data
    
    def getWindowState(self, zone):
        """Returns the state of the window for Zone zone"""
        data = self.getState(zone)['openWindow']
        return {'openWindow' : data}

    def getOpenWindowDetected(self, zone):
        """Returns whether an open window is detected."""
        data = self.getState(zone)
        if "openWindowDetected" in data:
            return {'openWindowDetected': data['openWindowDetected']}
        else:
            return {'openWindowDetected': False}

    def setOpenWindow(self, zone):
        """Sets the window in Zone zone to open"""
        # this can only be set if an open window was detected in this zone
        cmd = 'zones/%i/state/openWindow/activate' % (zone)
        data = self._apiCall(cmd, "POST", {}, True)
        return data

    def resetOpenWindow(self, zone):
        """Sets the window in zone Zone to closed"""
        cmd = 'zones/%i/state/openWindow' % zone
        data = self._apiCall(cmd, "DELETE", {}, True)
        return data
    
    # Ctor
    def __init__(self, username, password, timeout=10, http_session=None):
        """Performs login and save session cookie."""
        # HTTPS Interface

        # pylint: disable=C0103
        self._http_session = http_session if http_session else Session()
        self._loginV2(username, password)
        self.id = self.getMe()['homes'][0]['id']
