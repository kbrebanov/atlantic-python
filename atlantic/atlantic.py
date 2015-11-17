import os
import sys
import hmac
import json
import time
import uuid
import base64
import urllib
import urllib2
import hashlib

API_VERSION = "2010-12-30"
BASE_URL = "https://cloudapi.atlantic.net/?"
try:
    ANC_ACCESS_KEY_ID = os.environ['ANC_ACCESS_KEY_ID']
except KeyError:
    sys.exit("Environment variable ANC_ACCESS_KEY_ID is not set")
try:
    ANC_PRIVATE_KEY = os.environ['ANC_PRIVATE_KEY']
except KeyError:
    sys.exit("Environment variable ANC_PRIVATE_KEY is not set")

def generate_request():
    random_uuid = uuid.uuid4()
    time_since_epoch = int(time.time())
    string_to_sign = "%s%s" % (str(time_since_epoch), str(random_uuid))
    m = hmac.new(key=ANC_PRIVATE_KEY, msg=string_to_sign, digestmod=hashlib.sha256)
    signature = base64.b64encode(m.digest())
    request = {
        "Format": "json",
        "Version": API_VERSION,
        "ACSAccessKeyId": ANC_ACCESS_KEY_ID,
        "Timestamp": str(time_since_epoch),
        "Rndguid": str(random_uuid),
        "Signature": signature
    }
    signature = urllib.urlencode(request)
    return signature

def call_api(url):
    try:
        response = urllib2.urlopen(url)
    except URLError:
        sys.exit("Error calling Atlantic.net API")
    parsed_json = json.load(response)
    return parsed_json

def run_instance(servername, imageid, planname, vm_location, enablebackup="N", cloneimage="", serverqty=1):
    request = generate_request()
    url = "%s&Action=run-instance&%s&servername=%s&imageid=%s&planname=%s&vm_location=%s&enablebackup=%s&cloneimage=%s&serverqty=%s" % (BASE_URL, request, servername, imageid, planname, vm_location, enablebackup, cloneimage, serverqty)
    response = call_api(url)
    return response

def list_instances():
    request = generate_request()
    url = "%s&Action=list-instances&%s" % (BASE_URL, request)
    response = call_api(url)
    return response

def describe_instance(instanceid):
    request = generate_request()
    url = "%s&Action=describe-instance&%s&instanceid=%s" % (BASE_URL, request, instanceid)
    response = call_api(url)
    return response

def reboot_instance(instanceid, reboottype="soft"):
    request = generate_request()
    url = "%s&Action=reboot-instance&%s&instanceid=%s&reboottype=%s" % (BASE_URL, request, instanceid, reboottype)
    response = call_api(url)
    return response

def terminate_instance(instanceid):
    request = generate_request()
    url = "%s&Action=terminate-instance&%s&instanceid=%s" % (BASE_URL, request, instanceid)
    response = call_api(url)
    return response

def describe_image(imageid=""):
    request = generate_request()
    url = "%s&Action=describe-image&%s" % (BASE_URL, request)
    if imageid != "":
        url = "%s&imageid=%s" % (url, imageid)
    response = call_api(url)
    return response

def describe_plan(plan_name="", platform=""):
    request = generate_request()
    url = "%s&Action=describe-plan&%s" % (BASE_URL, request)
    if plan_name != "":
        url = "%s&plan_name=%s" % (url, plan_name)
    if platform != "":
        url = "%s&platform=%s" % (url, platform)
    response = call_api(url)
    return response
