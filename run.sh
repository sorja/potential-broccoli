#!/bin/bash
export FLASK_APP=vulnerableapp

if [ $1 = "--debug" ]; then
	export FLASK_DEBUG=true
fi
pip install -e .
flask run
