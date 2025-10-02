""" Somewhat nicer wrapper around ot_api.runs for lh related things """

from typing import Optional, Tuple

from ot_api.decorators import command, request_with_run_id
import ot_api.requestor as requestor
import ot_api.runs

def load_pipette(pipette_name, mount, run_id: Optional[str] = None) -> dict:
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
def add_mounted_pipettes(run_id=None) -> Tuple[Optional[dict], Optional[dict]]:
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
      "origin": "bottom",
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
      "origin": "bottom",
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
      "origin": "bottom",
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
def aspirate_in_place(
  volume: float,
  flow_rate: float,
  pipette_id,
  run_id: Optional[str]=None,
):
  params = {
    "flowRate": flow_rate,
    "volume": volume,
    "pipetteId": pipette_id
  }

  return ot_api.runs.enqueue_command("aspirateInPlace", params, intent="setup", run_id=run_id)

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
      "origin": "bottom",
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

@command
def dispense_in_place(
  volume: float,
  flow_rate: float,
  pipette_id,
  pushOut: bool = False,
  run_id: Optional[str]=None,
):
  params = {
    "flowRate": flow_rate,
    "volume": volume,
    "pipetteId": pipette_id,
    "pushOut": pushOut
  }

  return ot_api.runs.enqueue_command("aspirateInPlace", params, intent="setup", run_id=run_id)


@command
def move_arm(
  pipette_id: str,
  location_x: float,
  location_y: float,
  location_z: float,
  minimum_z_height: Optional[float],
  speed: Optional[float],
  force_direct: bool = False,
  run_id: Optional[str]=None
):
  params = {
    "pipetteId": pipette_id,
    "coordinates": {
      "x": location_x,
      "y": location_y,
      "z": location_z
    },
    "forceDirect": force_direct
  }

  if minimum_z_height is not None:
    params["minimumZHeight"] = minimum_z_height

  if speed is not None:
    params["speed"] = speed

  return ot_api.runs.enqueue_command("moveToCoordinates", params, intent="setup", run_id=run_id)

@command
def move_to_addressable_area_for_drop_tip(
  pipette_id: str,
  offset_x: float = 0,
  offset_y: float = 0,
  offset_z: float = 0,
  run_id: Optional[str]=None,
):
  params = {
    "pipetteId": pipette_id,
    "addressableAreaName": "fixedTrash",
    "wellName": "A1",
    "wellLocation": {
      "origin": "default",
      "offset": {
        "x": offset_x,
        "y": offset_y,
        "z": offset_z
      }
    },
    "alternateDropLocation": False
  }

  return ot_api.runs.enqueue_command("moveToAddressableAreaForDropTip", params,
                                     intent="setup", run_id=run_id)

@command
def drop_tip_in_place(pipette_id: str, run_id: Optional[str]=None):
  params = {
    "pipetteId": pipette_id
  }

  return ot_api.runs.enqueue_command("dropTipInPlace", params, intent="setup", run_id=run_id)
