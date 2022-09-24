""" Wrapper around the /runs endpoints"""

from typing import Optional

from ot_api.decorators import request_with_run_id
import ot_api.requestor as requestor

def create() -> str:
  data = requestor.post("/runs")
  return data["data"]["id"]

def get_all() -> list:
  data = requestor.get("/runs")
  return data["data"]

def get_run(run_id: str) -> dict:
  data = requestor.get(f"/runs/{run_id}")
  return data["data"]

@request_with_run_id
def get_current_run(run_id) -> str:
  return get_run(run_id)

@request_with_run_id
def get_command(command_id: str, run_id: Optional[str]):
  data = requestor.get(f"/runs/{run_id}/commands/{command_id}")
  return data

@request_with_run_id
def enqueue_command(command, params, intent, run_id):
  assert intent in ["setup", "protocol"]
  command = {
    "data": {
      "commandType": command,
      "params": params,
      "intent": intent
    }
  }
  resp = requestor.post(f"/runs/{run_id}/commands", command)
  return resp["data"]["id"]
