#!/bin/bash
set -eux

git fetch origin
git switch main
git pull origin main

python3 main.py --aiengine=0 --listen="0.0.0.0" --maxspeed ON


