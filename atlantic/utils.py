import base64
import hashlib
import hmac
import requests
import sys
import time
import uuid

API_VERSION = "2010-12-30"
API_ENDPOINT = "https://cloudapi.atlantic.net/"

class AtlanticError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class AtlanticBase(object):
    def __init__(self, access_key, private_key):
        self.api_version = API_VERSION
        self.api_endpoint = API_ENDPOINT
        self.access_key = access_key
        self.private_key = private_key
        self.format = "json"

    def _generate_signature(self, time_since_epoch, random_uuid):
        """
        This method generates a signature.

        All requests are required to include a signature computed using a
        base64 encoded, SHA256 encrypted hash generated from the request
        timestamp and a random GUID. The encryption needs to be done using
        your API private key.
        """
        string_to_sign = "%s%s" % (time_since_epoch, random_uuid)
        m = hmac.new(key=self.private_key, msg=string_to_sign, digestmod=hashlib.sha256)
        signature = base64.b64encode(m.digest())
        return signature

    def request(self, params):
        """
        This method creates a request and calls the Atlantic.net API.
        """
        random_uuid = uuid.uuid4()
        time_since_epoch = int(time.time())
        signature = self._generate_signature(time_since_epoch, random_uuid)
        required_params = {
            "Format": self.format,
            "Version": self.api_version,
            "ACSAccessKeyId": self.access_key,
            "Timestamp": str(time_since_epoch),
            "Rndguid": str(random_uuid),
            "Signature": signature
        }
        required_params.update(params)
        response = requests.get(self.api_endpoint, params=required_params)
        response_json = response.json()
        if "error" in response_json:
            message = response_json["error"]["message"]
            raise AtlanticError(message)
        return response_json
