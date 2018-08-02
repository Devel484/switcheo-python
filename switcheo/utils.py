#
# switcheo/utils.py
# Keith Smith
#
# For testnet requests to the Switcheo exchange

import json
import requests
import time


def get_epoch_milliseconds():
    return int(round(time.time() * 1000))


def stringify_message(message):
    """Return a JSON message that is alphabetically sorted by the key name

    Args:
        message
    """
    return json.dumps(message, sort_keys=True, separators=(',', ':'))


def reverse_hex(message):
    return "".join([message[x:x + 2] for x in range(0, len(message), 2)][::-1])


def num2hexstring(number, size=1, little_endian=False):
    """
    Converts a number to a big endian hexstring of a suitable size, optionally little endian
    :param {number} number
    :param {number} size - The required size in hex chars, eg 2 for Uint8, 4 for Uint16. Defaults to 2.
    :param {boolean} little_endian - Encode the hex in little endian form
    :return {string}
    """
    size = size * 2
    hexstring = hex(number)[2:]
    if len(hexstring) % size != 0:
        hexstring = ('0' * size + hexstring)[len(hexstring):]
    if little_endian:
        hexstring = reverse_hex(hexstring)
    return hexstring


def num2varint(num):
    """
    Converts a number to a variable length Int. Used for array length header

    :param: {number} num - The number
    :return: {string} hexstring of the variable Int.
    """
    # if (typeof num !== 'number') throw new Error('VarInt must be numeric')
    # if (num < 0) throw new RangeError('VarInts are unsigned (> 0)')
    # if (!Number.isSafeInteger(num)) throw new RangeError('VarInt must be a safe integer')
    if num < 0xfd:
        return num2hexstring(num)
    elif num <= 0xffff:
        # uint16
        return 'fd' + num2hexstring(number=num, size=4, little_endian=True)
    elif num <= 0xffffffff:
        # uint32
        return 'fe' + num2hexstring(number=num, size=8, little_endian=True)
    else:
        # uint64
        return 'ff' + num2hexstring(number=num, size=16, little_endian=True)


class Request(object):

    def __init__(self, api_url='https://test-api.switcheo.network/', api_version="/v2", timeout=30):
        self.url = api_url.rstrip('/')
        self.url = self.url + api_version
        self.timeout = timeout

    def get(self, path, params=None):
        """Perform GET request"""
        r = requests.get(self.url + path, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None, json_data=None, params=None):
        """Perform POST request"""
        r = requests.post(self.url + path, data=data, json=json_data, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()