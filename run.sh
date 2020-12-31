#!/bin/bash

export FLASK_APP=websshproxy
export FLASK_ENV=development
pip install -e .
flask run
