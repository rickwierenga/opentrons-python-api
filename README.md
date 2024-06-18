# Opentrons Python API

Simple (and currently incomplete) Python wrapper around the Opentrons HTTP API. Like https://github.com/Opentrons/opentrons/tree/edge/api-client, but in Python. This API is atomic and interactive.

This project is created for use with [PyLabRobot](https://github.com/pylabrobot/pylabrobot), but can be used however you like.

## Installation

- from pip

```sh
pip install opentrons-http-api-client
```

- from source

```sht 
git clone http://github.com/rickwierenga/opentrons-python-api
```

## Usage

Minimal example for simple liquid handling:

```py
import ot_api
ot_api.set_host("x.x.x.x") # find in OT app
ot_api.set_port(31950)     # default, so not really necessary

# Creating a run
run_id = ot_api.runs.create()
ot_api.set_run(run_id) # set run globally, alternative to `run_id` parameter for functions

# Add pipettes that are detected in hardware to the software
left_pipette, right_pipette = ot_api.lh.add_mounted_pipettes()
left_pipette_id = left_pipette["pipetteId"]

# Defining labware
data = ot_api.labware.define(labware_definition) # json from opentrons-shared-data
namespace, definition, version = data["data"]["definitionUri"].split("/")

# Adding labware
labware_id = "arbitrary id for labware"
ot_api.labware.add(
  load_name=definition,
  namespace=namespace,
  version=version,
  ot_location=1, # slot
  labware_id=labware_id
)

# Picking up a tip
ot_api.lh.pick_up_tip(labware_id=labware_id, well_name="A1", pipette_id=left_pipette_id)

# Aspirating
ot_api.lh.aspirate(labware_id=labware_id, well_name="A1", pipette_id=left_pipette_id,
                   flow_rate=10, volume=10)

# Dispensing
ot_api.lh.dispense(labware_id=labware_id, well_name="A1", pipette_id=left_pipette_id,
                   flow_rate=10, volume=10)

# Tip drop
ot_api.lh.drop_tip(labware_id=labware_id, well_name="A1", pipette_id=left_pipette_id)
```

**Note: the ot_api is blocking!**

## Notice

This project is not affiliated with Opentrons.

This project is created for the Sculpting Evolution group at the MIT Media Lab.

See [`LICENSE`](/LICENSE)
