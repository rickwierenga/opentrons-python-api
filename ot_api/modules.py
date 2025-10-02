from ot_api.decorators import command, request_with_run_id
import ot_api.requestor
import ot_api.runs


def list_connected_modules():
  """ List connected modules """
  return ot_api.requestor.get("/modules")["data"]

@command
def load_module(slot: int, model: str, module_id: str, run_id: str = None):
  """ Load a module into a slot """
  assert slot in range(1, 13)
  return ot_api.runs.enqueue_command("loadModule",
    params={"location": {
      "slotName": str(slot),
    },
    "model": model,
    "moduleId": module_id,
    }, intent="setup", run_id=run_id)

@command
def temperature_module_set_temperature(celsius: float, module_id: str, run_id: str = None):
  """ Set the temperature of a temperature module """
  return ot_api.runs.enqueue_command("temperatureModule/setTargetTemperature",
    {"celsius": celsius, "moduleId": module_id},
    intent="setup", run_id=run_id)

@command
def temperature_module_deactivate(module_id: str, run_id: str = None):
  """ Deactivate a temperature module """
  return ot_api.runs.enqueue_command("temperatureModule/deactivate",
    {"moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_open_lid(module_id: str, run_id: str = None):
  """ Open thermocycler lid """
  return ot_api.runs.enqueue_command("thermocycler/openLid",
    {"moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_close_lid(module_id: str, run_id: str = None):
  """ Close thermocycler lid """
  return ot_api.runs.enqueue_command("thermocycler/closeLid",
    {"moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_set_block_temperature(celsius: float, module_id: str, run_id: str = None):
  """ Set the temperature of a thermocycler block """
  return ot_api.runs.enqueue_command("thermocycler/setTargetBlockTemperature",
    {"celsius": celsius, "moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_set_lid_temperature(celsius: float, module_id: str, run_id: str = None):
  """ Set the temperature of a thermocycler lid """
  return ot_api.runs.enqueue_command("thermocycler/setTargetLidTemperature",
    {"celsius": celsius, "moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_deactivate_block(module_id: str, run_id: str = None):
  """ Deactivate thermocycler block """
  return ot_api.runs.enqueue_command("thermocycler/deactivateBlock",
    {"moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_deactivate_lid(module_id: str, run_id: str = None):
  """ Deactivate thermocycler lid """
  return ot_api.runs.enqueue_command("thermocycler/deactivateLid",
    {"moduleId": module_id}, intent="setup", run_id=run_id)

@command
def thermocycler_run_profile(profile: list, block_max_volume: float, module_id: str, run_id: str = None):
  """ Execute thermocycler profile run """
  return ot_api.runs.enqueue_command("thermocycler/runProfile",
    {"profile": profile, "blockMaxVolumeUl": block_max_volume,"moduleId": module_id}, intent="setup", run_id=run_id)

@request_with_run_id
def thermocycler_run_profile_no_wait(profile: list, block_max_volume: float, module_id: str, run_id: str = None):
  """ Enqueue thermocycler profile run without waiting for completion. """
  return ot_api.runs.enqueue_command("thermocycler/runProfile",
    {"profile": profile, "blockMaxVolumeUl": block_max_volume,"moduleId": module_id}, intent="setup", run_id=run_id)
