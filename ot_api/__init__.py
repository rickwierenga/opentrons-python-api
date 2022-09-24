HOST = None
PORT = 31950

run_id = None

def set_host(new_host):
  global HOST
  HOST = new_host

def set_port(new_port):
  global PORT
  PORT = new_port

def set_run(new_run_id):
  global run_id
  run_id = new_run_id

import ot_api.health as health
import ot_api.labware as labware
import ot_api.lh as lh
import ot_api.runs as runs
