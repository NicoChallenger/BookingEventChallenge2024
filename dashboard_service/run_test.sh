#!/bin/bash
set -a
pip install -r requirements.txt
pip install -r dev-requirements.txt
source venv/bin/activate
pytest .