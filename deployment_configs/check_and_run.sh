#!/bin/bash

# Define the port to be used for the server
PORT=8003

# Check if the specified port is already in use
if lsof -i :$PORT > /dev/null; then
    echo "Port $PORT is already in use. Killing all processes using the port."

    # Kill all processes using the specified port
    lsof -t -i :$PORT | xargs -r kill -9

    # Wait for 2 seconds before proceeding
    sleep 2
fi

# Execute Gunicorn with the specified configuration
exec /home/ubuntu/.cache/pypoetry/virtualenvs/taskbotpyrogram-c-Phk8m_-py3.12/bin/gunicorn \
    --workers 1 \
    --bind 0.0.0.0:8003 \
    -c /home/ubuntu/taskbot/deployment_configs/gunicorn_conf.py \
    -k uvicorn.workers.UvicornWorker \
    app:app
