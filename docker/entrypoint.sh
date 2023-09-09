#!/bin/bash
set -eux

git fetch origin
git switch main
git pull origin main
python3 cpp-main.py --listen="0.0.0.0" --maxspeed ON


