""" Actually making requests to the API """

import json
import requests
import urllib

import ot_api

headers = {
  "Opentrons-Version": "3",
}

def get_base() -> str:
  if ot_api.HOST is None:
    raise RuntimeError("ot_api host is not set, use ot_api.set_host('x.x.x.x')")
  base = f'http://{ot_api.HOST}:{ot_api.PORT}'
  return base

def get_url(path):
  return urllib.parse.urljoin(get_base(), path)

def _return_resp(resp: requests.Response) -> dict:
  if resp.status_code not in range(200, 300):
    raise Exception(resp.text)
  return json.loads(resp.text)

def get(path: str) -> dict:
  url = get_url(path)
  resp = requests.get(url, headers=headers)
  return _return_resp(resp)

def post(path: str, data=None) -> dict:
  url = get_url(path)
  if data is not None:
    data = json.dumps(data)
    headers["Content-Type"] = "application/json"
  resp = requests.post(url, headers=headers, data=data)
  return _return_resp(resp)

def delete(path):
  url = get_url(path)
  resp = requests.delete(url, headers=headers)
  return _return_resp(resp)
