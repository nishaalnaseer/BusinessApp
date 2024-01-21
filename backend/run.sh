#!/bin/bash
cd /home/pig/projects/TelegramApp/backend
source ./venv/bin/activate

uvicorn main:app --port 88 --host 0.0.0.0