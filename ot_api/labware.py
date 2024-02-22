""" Somewhat nicer wrapper around ot_api.runs for labware related things """

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
def add(load_name, namespace, version, slot: int, run_id: str = None, labware_id=None, display_name=None):
  """ Add a labware to a slot """
  assert slot in range(1, 13)
  data = {
    "location": {
      "slotName": str(slot),
    },
    "loadName": load_name,
    "namespace": namespace,
    "version": version,
    "labwareId": labware_id,
    "displayName": display_name,
  }
  return ot_api.runs.enqueue_command("loadLabware", data, intent="setup", run_id=run_id)
