""" Somewhat nicer wrapper around ot_api.runs for lh related things """

from typing import Optional, Tuple

from ot_api.decorators import command, request_with_run_id
import ot_api.requestor as requestor
import ot_api.runs

def load_pipette(pipette_name, mount, run_id: Optional[str] = None):
  assert mount in ["left", "right"]

  @command
  def _load_pipette(run_id=None):
    data = {
      "pipetteName": pipette_name,
      "mount": mount,
    }
    return ot_api.runs.enqueue_command("loadPipette", params=data, intent="setup", run_id=run_id)

  resp = _load_pipette(run_id=run_id)
  return resp["data"]["result"]

@request_with_run_id
def add_mounted_pipettes(run_id=None) -> Tuple[str, str]:
  mounted_pipettes = requestor.get("/pipettes")

  left_pipette = mounted_pipettes["left"]
  if left_pipette["name"] is not None:
    left = load_pipette(left_pipette["name"], "left", run_id=run_id)
    left["name"] = left_pipette["name"]
  else:
    left = None

  right_pipette = mounted_pipettes["right"]
  if right_pipette["name"] is not None:
    right = load_pipette(right_pipette["name"], "right", run_id=run_id)
    right["name"] = right_pipette["name"]
  else:
    right = None

  return left, right

@command
def pick_up_tip(
  labware_id: str,
  well_name: str,
  pipette_id: str,
  offset_x: float = 0,
  offset_y: float = 0,
  offset_z: float = 0,
  run_id: Optional[str]=None
):
  params = {
    "labwareId": labware_id,
    "wellName": well_name,
    "wellLocation": {
      "origin": "top",
      "offset": {
        "x": offset_x,
        "y": offset_y,
        "z": offset_z
      }
    },
    "pipetteId": pipette_id
  }
  return ot_api.runs.enqueue_command("pickUpTip", params, intent="setup", run_id=run_id)

@command
def drop_tip(
  labware_id: str,
  well_name: str,
  pipette_id: str,
  offset_x: float = 0,
  offset_y: float = 0,
  offset_z: float = 0,
  run_id: Optional[str]=None
):
  params = {
    "labwareId": labware_id,
    "wellName": well_name,
    "wellLocation": {
      "origin": "top",
      "offset": {
        "x": offset_x,
        "y": offset_y,
        "z": offset_z
      }
    },
    "pipetteId": pipette_id
  }

  return ot_api.runs.enqueue_command("dropTip", params, intent="setup", run_id=run_id)

@command
def aspirate(
  labware_id: str,
  well_name: str,
  volume: float,
  flow_rate: float,
  pipette_id,
  run_id: Optional[str]=None,
  offset_x: float = 0,
  offset_y: float = 0,
  offset_z: float = 0,
):
  params = {
    "labwareId": labware_id,
    "wellName": well_name,
    "wellLocation": {
      "origin": "top",
      "offset": {
        "x": offset_x,
        "y": offset_y,
        "z": offset_z
      },
    },
    "flowRate": flow_rate,
    "volume": volume,
    "pipetteId": pipette_id
  }

  return ot_api.runs.enqueue_command("aspirate", params, intent="setup", run_id=run_id)

@command
def dispense(
  labware_id: str,
  well_name: str,
  volume: float,
  flow_rate: float,
  pipette_id,
  run_id: Optional[str]=None,
  offset_x: float = 0,
  offset_y: float = 0,
  offset_z: float = 0,
):
  params = {
    "labwareId": labware_id,
    "wellName": well_name,
    "wellLocation": {
      "origin": "top",
      "offset": {
        "x": offset_x,
        "y": offset_y,
        "z": offset_z
      },
    },
    "flowRate": flow_rate,
    "volume": volume,
    "pipetteId": pipette_id
  }

  return ot_api.runs.enqueue_command("dispense", params, intent="setup", run_id=run_id)
