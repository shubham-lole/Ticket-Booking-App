#!/bin/bash

# Backend setup
echo "Setting up backend..."
cd backend
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python3 mail.py &
echo "Backend setup complete."

# Frontend setup
echo "Setting up frontend..."
cd ../frontend
npm install
echo "Frontend setup complete."

# Celery setup
echo "Setting up Celery..."
cd ../backend
echo "Starting Celery beat..."
source local_beat.sh &
echo "Starting Celery tasks..."
source local_workers.sh &
echo "Celery setup complete."

# Open the application
echo "Starting the application..."
echo "Navigate to http://localhost:8080"
npm run serve

