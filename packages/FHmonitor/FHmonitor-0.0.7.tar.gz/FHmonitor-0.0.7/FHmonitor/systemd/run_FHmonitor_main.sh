#!/bin/bash

PROJ_PATH=/home/pi/projects/FHmonitor_project
. $PROJ_PATH/venv/bin/activate
python3 $PROJ_PATH/FHmonitor/FHmonitor/FHmonitor_main.py
