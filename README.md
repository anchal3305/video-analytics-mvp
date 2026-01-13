# Multi-Camera Video Analytics MVP

An end-to-end video analytics platform MVP that ingests camera streams, runs AI-based computer vision, applies zone-based rules, generates events, exposes REST APIs, and visualizes results in a web dashboard.

This project is inspired by modern enterprise video analytics platforms such as Milestone VMS, BriefCam, Avigilon, and Frigate, and follows a modular, scalable, privacy-first architecture.

## Objective

Build a working MVP that demonstrates:

RTSP / camera stream ingestion

Real-time AI inference (object detection)

Rule-based analytics (intrusion & loitering)

Event generation and persistence

REST APIs for querying analytics data

A lightweight dashboard for operators

Clean architecture with clear separation of concerns

## System Overview

High-level pipeline:

Camera → Ingestion → AI Inference → Rules Engine → Events → Database → API → Dashboard

What happens in real time:

Camera frames are ingested from RTSP / webcam

YOLO detects people in frames

Zone-based rules are evaluated

Intrusion / loitering events are generated

Events are stored in SQLite

FastAPI exposes events via REST APIs

Dashboard fetches and displays events live

## Architecture

The system is structured as a modular monorepo:

video-analytics-mvp/

├── ingestion/      # RTSP ingestion & frame handling

├── inference/      # YOLO-based object detection

├── rules/          # Zones and rule engine (intrusion, loitering)

├── events/         # Event schema & SQLite persistence

├── api/            # FastAPI backend

├── ui/             # Dashboard (HTML/CSS/JS)

├── README.md

└── .gitignore

#### Key design principles:

Separation of concerns (ingestion ≠ inference ≠ rules ≠ API ≠ UI)

Event-driven analytics

Local-first & privacy-aware (store metadata, not full video)

Extensible for multi-camera & multi-model use cases

## Features
### Implemented (MVP)
Video Ingestion

RTSP / webcam support

Auto-reconnect on failure

FPS tracking

Camera online/offline status

AI Inference

YOLO-based person detection

Confidence scores & bounding boxes

Frame-skipping for performance

Analytics & Rules

Zone definition (rectangular zones)

Intrusion detection (person enters restricted zone)

Loitering detection (person remains > N seconds)

Time-based state tracking

Event Management

Structured event schema

SQLite persistence

Metadata-only storage (privacy-first)

#### Backend API (FastAPI)

GET /health

GET /events

GET /events/{id}

GET /cameras

POST /cameras

CORS enabled for dashboard access

Swagger/OpenAPI docs

Dashboard UI

Camera event feed

Live auto-refresh

Event metadata view

Lightweight static frontend

## Tech Stack

Python 3.10

OpenCV – video ingestion

YOLO (Ultralytics) – object detection

FastAPI – backend APIs

SQLite – event storage

HTML / CSS / JavaScript – dashboard UI

## How to Run
1. Clone the Repository
git clone https://github.com/anchal3305/video-analytics-mvp.git

cd video-analytics-mvp

3. Install Dependencies
   
pip install -r requirements.txt


(If no requirements.txt yet, install manually: fastapi, uvicorn, opencv-python, ultralytics)

3️. Start the API

uvicorn api.main:app --reload


API Docs: 

http://127.0.0.1:8000/docs

Health Check: 

http://127.0.0.1:8000/health

4️. Start Video Analytics (Ingestion + AI)

python -m ingestion.rtsp_reader


Uses webcam by default (rtsp_url=1)

Displays live video with detections & zones

Press q to stop

5️. Start Dashboard UI
cd ui/dashboard
python -m http.server 5500


Open in browser:

http://127.0.0.1:5500

## How to Test

Start all three components:

API

Ingestion

UI

Walk into the blue “Restricted Area” box

Observe:

Intrusion events appear

Loitering events after configured time

#### Verify:

Events stored in SQLite

Events visible via /events

Dashboard auto-updates

## Security & Privacy Considerations

No raw video stored

Only event metadata persisted

Local-first processing

CORS explicitly configured

Ready for role-based access control (future)

## Performance Notes

Frame skipping reduces inference load

Rules engine maintains minimal state

Architecture supports horizontal scaling

Designed for multi-camera extension

## Known Limitations (MVP)

Single-camera demo setup

In-memory camera registry

Simple rectangular zones only

No authentication / authorization

No event deduplication yet

## Future Improvements

If extended further:

Multi-camera & multi-site support

Polygon zone editor in UI

Event clip recording (pre/post seconds)

Role-based access control

MQTT / webhook event publishing

Advanced search & heatmaps

PostgreSQL / OpenSearch backend

Hardware acceleration (OpenVINO / DeepStream)

## Demo Flow (3–5 Minutes)

Start API → show /docs

Start ingestion → show live detection

Walk into zone → intrusion event

Stay in zone → loitering event

Open dashboard → show events live

Explain architecture & design choices

## Key Takeaway

This project demonstrates how raw video → AI → contextual rules → actionable events can be built into a scalable, modular video analytics platform, following patterns used in real enterprise systems.

## Author

### Anchal Gupta
### BSc IT | Data Science & AI
### Interested in AI/ML Systems & Applied Computer Vision
