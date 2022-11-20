#!/bin/bash
python3 -m venv venv
venv/bin/pip install --upgrade --upgrade-strategy=eager pip
venv/bin/pip install --upgrade --upgrade-strategy=eager setuptools
venv/bin/pip install --upgrade --upgrade-strategy=eager -r requirements.txt
