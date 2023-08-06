"""
A very basic module for Eurotronic CometBlue thermostats.
They are identical to the Sygonix, Xavax Bluetooth thermostats

This version is based on the bluepy module. 
Currently only current and target temperature in manual mode is supported, nothing else.
Parts were taken from the cometblue module by im-0
"""
import logging
import struct

from bluepy import btle

_LOGGER = logging.getLogger(__name__)

COMETBLUE_SERVICE = "47E9EE00-47E9-11E4-8939-164230D1DF67"
PASSWORD_CHAR = "47e9ee30-47e9-11e4-8939-164230d1df67"
TEMPERATURE_CHAR = "47e9ee2b-47e9-11e4-8939-164230d1df67"
BATTERY_CHAR = "47e9ee2c-47e9-11e4-8939-164230d1df67"
STATUS_CHAR = "47e9ee2a-47e9-11e4-8939-164230d1df67"
DATETIME_CHAR = "47e9ee01-47e9-11e4-8939-164230d1df67"
MODEL_CHAR = "47e9ee2d-47e9-11e4-8939-164230d1df67"
_PIN_STRUCT_PACKING = '<I'
_DATETIME_STRUCT_PACKING = '<BBBBB'
_DAY_STRUCT_PACKING = '<BBBBBBBB'


def _encode_datetime(dt):
    if dt.year < 2000:
        raise RuntimeError('Invalid year')
    return struct.pack(
        _DATETIME_STRUCT_PACKING,
        dt.minute,
        dt.hour,
        dt.day,
        dt.month,
        dt.year - 2000)


class CometBlueStates:
    """CometBlue Thermostat States"""
    _TEMPERATURES_STRUCT_PACKING = '<bbbbbbb'
    _STATUS_STRUCT_PACKING = '<BBB'

    _STATUS_BITMASKS = {
        'childlock': 0x80,
        'manual_mode': 0x1,
        'adapting': 0x400,
        'not_ready': 0x200,
        'installing': 0x400 | 0x200 | 0x100,
        'motor_moving': 0x100,
        'antifrost_activated': 0x10,
        'satisfied': 0x80000,
        'low_battery': 0x800,
        'unknown': 0x2000
    }

    def __init__(self):
        self.firmware_rev = None
        self.manufacturer = None
        self.model = None
        self.name = None
        self.software_rev = None
        self.target_temperature = None
        self.target_temp_l = None
        self.target_temp_h = None
        self.offset_temperature = None
        self.window_open_detection = None
        self.window_open_minutes = None
        self._status = dict()
        self._battery_level = None
        self._current_temp = None

    @property
    def battery_level(self):
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        self._battery_level = ord(value)

    @property
    def manual_mode(self):
        return self._status.get('manual_mode', False)

    @manual_mode.setter
    def manual_mode(self, value):
        self._status['manual_mode'] = value

    @property
    def status(self):
        def encode_status(value):
            status_dword = 0
            for key, state in value.items():
                if not state:
                    continue
                if key not in CometBlueStates._STATUS_BITMASKS:
                    continue
                status_dword |= CometBlueStates._STATUS_BITMASKS[key]
            value = struct.pack('<I', status_dword)
            # downcast to 3 bytes
            return struct.pack(CometBlueStates._STATUS_STRUCT_PACKING, *[int(byte) for byte in value[:3]])

        # check for changed status with 'is not None'
        if len(self._status) == 0:
            return None
        else:
            _LOGGER.debug("Updating Status to %s", self._status)
            return encode_status(self._status)

    @status.setter
    def status(self, val):
        def decode_status(value):
            state_bytes = struct.unpack(CometBlueStates._STATUS_STRUCT_PACKING, value)
            state_dword = struct.unpack('<I', value + b'\x00')[0]

            report = {}
            masked_out = 0
            for key, mask in CometBlueStates._STATUS_BITMASKS.items():
                report[key] = bool(state_dword & mask == mask)
                masked_out |= mask

            report['state_as_dword'] = state_dword
            report['unused_bits'] = state_dword & ~masked_out

            return report

        if val is None:
            self._status = dict()
        else:
            self._status = decode_status(val)

    @property
    def temperature(self):
        """Current temperature"""
        return self._current_temp

    @property
    def temperatures(self):
        def float_to_int(value):
            """Encode float for CometBlue update, returns value * 2.0, if value is set, else -128"""
            return -128 if value is None else int(value * 2.0)

        def int_to_int(value):
            """Encode float for CometBlue update, returns value, if value is set, else -128"""
            return -128 if value is None else int(value)

        temps = {
            'current_temp': -128,  # current temp
            'manual_temp': float_to_int(self.target_temperature),
            'target_temp_l': float_to_int(self.target_temp_l),
            'target_temp_h': float_to_int(self.target_temp_h),
            'offset_temp': float_to_int(self.offset_temperature),
            'window_open_detection': int_to_int(self.window_open_detection),
            'window_open_minutes': int_to_int(self.window_open_minutes),
        }
        _LOGGER.debug("Updating Temperatures to target_temp={%d}", temps['manual_temp'])

        data = struct.pack(
            CometBlueStates._TEMPERATURES_STRUCT_PACKING,
            *temps.values(),
        )
        return data

    @temperatures.setter
    def temperatures(self, value):
        current_temp, manual_temp, target_low, target_high, offset_temp, window_open_detect, window_open_minutes = \
            struct.unpack(CometBlueStates._TEMPERATURES_STRUCT_PACKING, value)
        self._current_temp = current_temp / 2.0
        self.target_temperature = manual_temp / 2.0
        self.target_temp_l = target_low / 2.0
        self.target_temp_h = target_high / 2.0
        self.offset_temperature = offset_temp / 2.0
        self.window_open_detection = window_open_detect
        self.window_open_minutes = window_open_minutes


class CometBlue:
    """CometBlue Thermostat """

    def __init__(self, address, pin):
        super(CometBlue, self).__init__()
        self._address = address
        self._conn = btle.Peripheral()
        self._pin = pin
        self.available = False
        self._handles = dict()
        self._current = CometBlueStates()
        self._target = CometBlueStates()

    def connect(self):
        """Connect to thermostat and send PIN"""
        _LOGGER.debug("Connecting to device %s", self._address)

        try:
            self._conn.connect(self._address)
        except btle.BTLEException as exc:
            _LOGGER.debug("Unable to connect to the device %s, retrying.", self._address, exc_info=exc)
            try:
                self._conn.connect(self._address)
            except btle.BTLEException as exc:
                _LOGGER.debug("Second connection try to %s failed.", self._address, exc_info=exc)
                raise

        if len(self._handles) == 0:
            _LOGGER.debug("Discovering characteristics %s", self._address)
            try:
                service = self._conn.getServiceByUUID(COMETBLUE_SERVICE)
                chars = service.getCharacteristics()
                self._handles = {str(a.uuid): a.getHandle() for a in chars}
            except btle.BTLEException as exc:
                _LOGGER.debug("Could not discover characteristics %s", self._address, exc_info=exc)
                raise

        # authenticate with PIN and initialize static values
        try:
            data = struct.pack(_PIN_STRUCT_PACKING, self._pin)
            self._conn.writeCharacteristic(self._handles[PASSWORD_CHAR], data, withResponse=True)
        except btle.BTLEException as exc:
            _LOGGER.debug("Can't set PIN for device %s. Is pin=%s correct?", self._address, self._pin,
                          exc_info=exc)
            raise

    def disconnect(self):
        """Disconnect from thermostat"""
        self._conn.disconnect()
        _LOGGER.debug("Disconnected from device %s", self._address)

    def should_update(self):
        """
        Signal necessity to call update() on next cycle because values need
        to be updated or last update was unsuccessfull.
        """
        return (not self.available
                or self._target.target_temperature is not None
                or self._target.status is not None)

    @property
    def target_temperature(self):
        return self._current.target_temperature

    @target_temperature.setter
    def target_temperature(self, temperature):
        """Set manual temperature. Call update() afterwards"""
        self._target.target_temperature = temperature

    @property
    def current_temperature(self):
        return self._current.temperature

    @property
    def model(self):
        return self._current.model

    @property
    def battery_level(self):
        return self._current.battery_level

    @property
    def manual_mode(self):
        return self._current.manual_mode

    @manual_mode.setter
    def manual_mode(self, mode):
        """set manual/auto mode. Call update() afterwards"""
        self._target.manual_mode = mode

    def update(self):
        """Communicate with device, first try to write new values, then read from device"""
        current = self._current
        target = self._target

        try:
            self.connect()

            if current.model is None:
                current.model = str(self._conn.readCharacteristic(self._handles[MODEL_CHAR]))

            if target.target_temperature is not None:
                self._conn.writeCharacteristic(self._handles[TEMPERATURE_CHAR], target.temperatures,
                                               withResponse=True)
                target.target_temperature = None

            if target.status is not None:
                self._conn.writeCharacteristic(self._handles[STATUS_CHAR], target.status,
                                               withResponse=True)
                target.status = None

            current.temperatures = self._conn.readCharacteristic(self._handles[TEMPERATURE_CHAR])

            current.status = self._conn.readCharacteristic(self._handles[STATUS_CHAR])

            current.battery_level = self._conn.readCharacteristic(self._handles[BATTERY_CHAR])
        except btle.BTLEGattError as exc:
            _LOGGER.error("Can't read/write cometblue data (%s). Did you set the correct PIN?", self._address,
                          exc_info=exc)
            self.available = False
        except btle.BTLEException as exc:
            _LOGGER.error("Can't connect to cometblue (%s). Did you set the correct PIN?", self._address, exc_info=exc)
            self.available = False
        else:
            self.available = True
        finally:
            self.disconnect()
