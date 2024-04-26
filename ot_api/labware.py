""" Somewhat nicer wrapper around ot_api.runs for labware related things """

from typing import Union

from ot_api.decorators import request_with_run_id, command
import ot_api.requestor
import ot_api.runs


@request_with_run_id
def define(labware_def, run_id=None):
  """ Define a labware in the current run. Labware can be added with the `add` command """
  data = {"data": labware_def}
  return ot_api.requestor.post(f"/runs/{run_id}/labware_definitions", data)

@request_with_run_id
def undefine(labware_def_id, run_id=None):
  """ Remove a labware definition """
  return ot_api.requestor.delete(f"/runs/{run_id}/labware_definitions/{labware_def_id}")

@command
def add(load_name, namespace, version, ot_location: Union[int, str], run_id: str = None, labware_id=None, display_name=None):
  """ Add a labware to a slot """
  if isinstance(ot_location, int):
    if not ot_location in range(1, 13):
      raise ValueError("Invalid slot")
    location = {
      "slotName": str(ot_location),
    }
  else:
    location = {
      "moduleId": ot_location,
    }

  data = {
    "location": location,
    "loadName": load_name,
    "namespace": namespace,
    "version": version,
    "labwareId": labware_id,
    "displayName": display_name,
  }
  return ot_api.runs.enqueue_command("loadLabware", data, intent="setup", run_id=run_id)

@command
def move_labware(labware_id, deck_slot: str  = None, module: str = None,
                 destination_labware_id: str = None, off_deck=False, run_id: str = None):
  """ Move a labware to a new location

  Specify exactly one of `deck_slot`, `module` and `destination_labware_id`, or set `off_deck` to True
  """

  if not sum([deck_slot is not None, module is not None, destination_labware_id is not None, off_deck]) == 1:
    raise ValueError("Specify exactly one of `deck_slot`, `module`, or `destination_labware_id` or set `off_deck` to True")

  if deck_slot is not None:
    new_location = {"slotName": deck_slot}
  elif module is not None:
    new_location = {"moduleId": module}
  elif destination_labware_id is not None:
    new_location = {"labwareId": destination_labware_id}
  else:
    new_location = "offDeck"

  data = {
    "labwareId": labware_id,
    "newLocation": new_location,
    "strategy": "manualMoveWithoutPause"
  }
  return ot_api.runs.enqueue_command("moveLabware", data, intent="setup", run_id=run_id)
