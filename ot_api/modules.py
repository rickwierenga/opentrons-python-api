from ot_api.decorators import command
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
