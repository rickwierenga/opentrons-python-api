""" Actually making requests to the API """

import json
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

def _return_resp(resp) -> dict:
  if not (200 <= resp.getcode() < 300):
    raise Exception(resp.read().decode())
  return json.loads(resp.read().decode())

def get(path: str) -> dict:
  url = get_url(path)
  req = urllib.request.Request(url, headers=headers, method="GET")
  with urllib.request.urlopen(req) as resp:
    return _return_resp(resp)

def post(path: str, data=None) -> dict:
  url = get_url(path)
  body = None
  req_headers = headers.copy()
  if data is not None:
    body = json.dumps(data).encode("utf-8")
    req_headers["Content-Type"] = "application/json"
  req = urllib.request.Request(url, headers=req_headers, data=body, method="POST")
  with urllib.request.urlopen(req) as resp:
    return _return_resp(resp)

def delete(path: str) -> dict:
  url = get_url(path)
  req = urllib.request.Request(url, headers=headers, method="DELETE")
  with urllib.request.urlopen(req) as resp:
    return _return_resp(resp)
