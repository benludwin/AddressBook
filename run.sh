#!/bin/bash

# Checking for sqlite3 package
if python -c "import sqlite3" &> /dev/null; then
    echo "[Installation]: sqlite3 module for python found"
else
    echo "[Installation]: sqlite3 module for python not found. Please install."
    exit 1;
fi

echo "[Installation]: Creating virtual environment"
python3 -m venv AddressServer

# Activating the environment
echo "[Installation]: Activating the virtual environment."
#. AddressServer/bin/activate

# Starting the server
echo "[Installation]: Starting the server"
export FLASK_APP=core_logic.py
flask run
echo "[Installation]: The server is successfully up and running"
