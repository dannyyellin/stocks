import requests
import json
import sys


def http_get(resource: str):
    # print("serviceController::GET: resource = ", resource)
    response = requests.get(url=resource, headers={"Content-Type": "application/json"})
    return response


def http_delete(resource: str):
    response = requests.delete(url=resource, headers={"Content-Type": "application/json"})
    return response


def http_post(resource: str, data: {}):
    # print("in http_post.  data = ", data)
    sys.stdout.flush()
    response = requests.post(url=resource, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response

def http_post_xml(resource: str, data: {}):
    # print("in http_post.  data = ", data)
    # sys.stdout.flush()
    response = requests.post(url=resource, headers={"Content-Type": "application/xml"}, data=json.dumps(data))
    return response


def http_put(resource: str, data: {}):
    response = requests.put(url=resource, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response


def post_raw(resource: str, data:{}, headers: {}):
    response = requests.post(url=resource, headers=headers, data=json.dumps(data))
    return response
