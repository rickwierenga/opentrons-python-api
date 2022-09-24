""" Decorators for the ot_api functions """

import datetime
import functools

import opentrons.protocol_engine.errors as ot_errors

import ot_api


def request_with_run_id(f):
  """ get run_id from param, if given, otherwise __init__, if given, otherwise raise error """

  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    if "run_id" not in kwargs:
      run_id = ot_api.run_id
      if run_id is None:
        raise TypeError("No run_id given. Please pass run_id as a parameter or use ot_api.set_run_id()")
      kwargs["run_id"] = run_id

    try:
      return f(*args, **kwargs)
    except TypeError as e:
      if "run_id" in str(e):
        raise TypeError("Error calling function. Did you not pass run_id as a kwarg?")
      raise e

  return wrapper


def command(f, timeout=30):
  """ Decorator for commands. Uses request_with_run_id. Waits for success or failure, potentially raising an error. """

  def get_ot_error(name) -> ot_errors.ProtocolEngineError:
    return getattr(ot_errors, name)
  
  @request_with_run_id
  def wrapper(*args, **kwargs):
    command_id = f(*args, **kwargs)

    end = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    while datetime.datetime.now() < end:
      result = ot_api.runs.get_command(command_id, run_id=kwargs["run_id"])
    
      if result["data"]["status"] == "failed":
        error_data = result["data"]["error"]
        error_class = get_ot_error(error_data["errorType"])
        raise error_class(error_data["detail"])
      elif result["data"]["status"] in ["queued", "running"]:
        continue
 
      return result
    
    raise RuntimeError("Command timed out")

  return wrapper
