# TicketBooking v2

A ticket booking platform built with flask and vuejs

## About

Ticketbooking with features to handle multiple theaters with multiple shows

## Features

flask backend with jwt authentication based token and included redis caching along with celery-redis backend jobs for periodic functions.

## Getting Started

## For running the backend app

1. Create a local enviroment in backend folder
2. python3 -m venv myenv
3. source myenv/bin/activate
4. pip install -r requirements.txt
5. python3 mail.py

## For running the frontend app

1. Install vue-cli in frontend folder
   npm install
2. npm run serve

## For running celery beat and celery tasks

1. In two different tabs in backend folder run the following scripts seperately
   source local_beat.sh
   source local_workers.sh

## Usage

Navigate to the following url after hosting
http://localhost:8080

## API Documentation

The api specifications are provided in # openapi.yaml

## Contact

Shubham Prakash Lole
21f2001330@ds.study.iitm.ac.in

---
