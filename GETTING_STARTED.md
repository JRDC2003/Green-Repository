# Getting Started Guide

Welcome to Green Repository! This guide will help you set up and start using the server.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git
- Docker & Docker Compose (optional, for database)

## Installation

### Step 1: Clone & Setup

```bash
cd Green-Repository
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env if needed (optional for development)
```

### Step 3: Start the Server

**Option A: Simple (SQLite database)**
```bash
bash start.sh
# Server runs at http://localhost:8000
```

**Option B: With PostgreSQL (using Docker)**
```bash
# Start database
docker-compose up -d

# Update .env with PostgreSQL URL
# DATABASE_URL=postgresql://green_user:green_password@localhost:5432/green_repository

# Run server
bash start.sh
```

## Testing the API

### 1. Interactive Docs
Visit http://localhost:8000/docs - Try endpoints directly in browser

### 2. Send Test Data

**Example 1: Single Sensor Reading**
```bash
curl -X POST "http://localhost:8000/api/v1/iot/sensor-reading" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "forest_cam_01",
    "timestamp": "2024-05-21T14:30:00",
    "latitude": 1.3521,
    "longitude": 103.8198,
    "sensor_type": "camera",
    "raw_data": {
      "frame_count": 1500,
      "resolution": "1920x1080"
    },
    "metadata": {
      "location": "Northern Forest Zone",
      "weather": "clear"
    }
  }'
```

**Example 2: Batch Sensor Readings**
```bash
curl -X POST "http://localhost:8000/api/v1/iot/sensor-readings/batch" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "device_id": "thermal_01",
      "timestamp": "2024-05-21T14:30:00",
      "latitude": 1.3525,
      "longitude": 103.8200,
      "sensor_type": "thermal",
      "raw_data": {"temperature": 28.5}
    },
    {
      "device_id": "motion_01",
      "timestamp": "2024-05-21T14:31:00",
      "latitude": 1.3530,
      "longitude": 103.8205,
      "sensor_type": "motion",
      "raw_data": {"motion_detected": true}
    }
  ]'
```

**Example 3: Get Device Readings**
```bash
curl "http://localhost:8000/api/v1/iot/sensor-readings/forest_cam_01?limit=10"
```

**Example 4: Run AI Detection**
```bash
curl -X POST "http://localhost:8000/api/v1/ai/detect/sensor-data?sensor_reading_id=1"
```

**Example 5: Get Recent Detections**
```bash
curl "http://localhost:8000/api/v1/stream/detections/recent?hours=24&limit=10"
```

## Project Structure Overview

```
app/
├── main.py              # FastAPI app & routes registration
├── config/
│   └── settings.py      # Load config from environment
├── models/
│   ├── sensor_data.py   # Request/response schemas
│   └── orm.py           # Database models
├── routes/
│   ├── iot.py           # /api/v1/iot/* endpoints
│   ├── stream.py        # /api/v1/stream/* endpoints
│   └── ai.py            # /api/v1/ai/* endpoints
├── services/
│   └── db.py            # Database connection & queries
├── ai/
│   └── detector.py      # Detection model & inference
└── utils/
    └── __init__.py      # Helper functions
```

## Key Features Explained

### 1. IoT Data Ingestion
- Receive sensor data from distributed devices
- Store readings with GPS coordinates
- Batch upload support for efficiency
- Auto timestamp if not provided

### 2. Real-time Streaming
- WebSocket endpoint for live updates
- Zone-based detection alerts
- Mobile app integration ready

### 3. AI Detection
- Pluggable model architecture
- Currently has mock detector (replace with your model)
- Confidence thresholding
- Result caching & storage

## Customization

### Replace Mock AI Model

1. Train your model using your dataset
2. Save as pickle file: `models/detector.pkl`
3. Or update `app/ai/detector.py` to load your model format

```python
# Example: Load TensorFlow model
import tensorflow as tf

model = tf.keras.models.load_model('path/to/model.h5')
predictions = model.predict(data)
```

### Add Database Migrations

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Connect Mobile App

Your mobile app should:
1. POST sensor readings to `/api/v1/iot/sensor-reading`
2. Connect WebSocket to `/api/v1/stream/ws/live-detections`
3. GET detections from `/api/v1/stream/detections/recent`

Example WebSocket connection (JavaScript):
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/stream/ws/live-detections');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Detection alert:', data);
};
```

## Troubleshooting

**Port 8000 already in use?**
```bash
lsof -i :8000  # Find what's using it
kill -9 <PID>  # Kill the process
# Or use different port:
uvicorn app.main:app --port 8001
```

**Database errors?**
```bash
# Reset SQLite database
rm green_repository.db
# Or PostgreSQL:
docker-compose down -v
docker-compose up -d
```

**Import errors?**
```bash
# Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Next Steps

1. ✅ Server running locally
2. 📱 Connect your mobile app to the API
3. 🤖 Train and integrate your AI model
4. 🌍 Set up forest zone definitions
5. 📊 Configure alert rules and severity levels
6. ☁️ Deploy to production server

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [WebSocket Guide](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## Support

- Check logs: `tail -f server.log`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Happy coding! 🌲
