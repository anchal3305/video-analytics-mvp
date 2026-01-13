# Video Analytics MVP – Project Plan

## Objective
Build a working MVP of a multi-camera video analytics platform that ingests RTSP streams,
runs AI-based detection, generates rule-based events, and displays them in a dashboard.

## MVP Scope
- RTSP ingestion (start with 1 camera)
- Person detection using YOLO
- Zone-based rules:
  - Intrusion detection
  - Loitering detection
- Event generation with snapshots
- SQLite-based event storage
- REST API (FastAPI)
- Simple web dashboard

## Out of Scope (for MVP)
- Advanced multi-object tracking
- GPU optimization
- Enterprise authentication
- Long-term video storage

## Architecture (Logical)
- Ingestion: RTSP stream reader
- Inference: Object detection model
- Rules Engine: Zone + time-based logic
- Event Store: SQLite
- API: FastAPI
- UI: Web dashboard

## Inspiration / Research Targets
- Milestone (camera & VMS concepts)
- BriefCam (Review / Respond / Research)
- Avigilon (alert-driven workflows)
- Frigate (local-first, event-based analytics)
