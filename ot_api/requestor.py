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

def make_request(req) -> dict:
  try:
    with urllib.request.urlopen(req) as resp:
      return json.loads(resp.read().decode())
  except urllib.error.HTTPError as e:
    raise Exception(e.read().decode())


def get(path: str) -> dict:
  return make_request(urllib.request.Request(get_url(path), headers=headers, method="GET"))

def post(path: str, data=None) -> dict:
  body = None
  req_headers = headers.copy()
  if data is not None:
    body = json.dumps(data).encode("utf-8")
    req_headers["Content-Type"] = "application/json"
  return make_request(urllib.request.Request(get_url(path), headers=req_headers, data=body, method="POST"))

def delete(path: str) -> dict:
  return make_request(urllib.request.Request(get_url(path), headers=headers, method="DELETE"))
