# 🌲 Project Architecture & Next Steps

## What I've Created

Your Green Repository server has the following components:

### Core Server Structure
- **FastAPI Application** - Modern, fast Python web framework
- **SQLAlchemy ORM** - Database models for storing data
- **WebSocket Support** - Real-time streaming to mobile apps
- **RESTful API** - Clean endpoints for all operations

### Key Directories

```
app/
├── main.py                 # Entry point - runs the server
├── config/settings.py      # Configuration management
├── models/
│   ├── sensor_data.py      # Data schemas (what you send)
│   └── orm.py              # Database models (how data is stored)
├── routes/
│   ├── iot.py              # Receive data from IoT devices
│   ├── stream.py           # Real-time WebSocket for mobile app
│   └── ai.py               # AI inference endpoints
├── services/db.py          # Database connections
└── ai/detector.py          # AI detection logic (placeholder)
```

## The Three Main APIs

### 1️⃣ IoT Data Ingestion (`/api/v1/iot`)
Your forest sensors (cameras, thermal, motion) send data here:
```
POST /sensor-reading           → Store single reading
POST /sensor-readings/batch    → Store multiple readings
GET /sensor-readings/{device}  → Retrieve stored data
```

### 2️⃣ Real-Time Streaming (`/api/v1/stream`)
Your mobile app connects here for live alerts:
```
WS /ws/live-detections        → WebSocket for alerts
GET /detections/recent        → Get last 24h detections
GET /detections/by-zone/{id}  → Get zone-specific detections
```

### 3️⃣ AI Detection (`/api/v1/ai`)
Run machine learning models:
```
POST /detect/image            → Analyze image for threats
POST /detect/sensor-data      → Analyze sensor readings
GET /health                   → Check AI service status
```

## Data Flow

```
IoT Device (Camera/Thermal)
    ↓
POST /api/v1/iot/sensor-reading
    ↓
Database (stores raw data)
    ↓
Run AI Detection
    ↓
WebSocket Alert to Mobile App
    ↓
Mobile Dashboard Shows Alert
```

## Installation Steps

### 1. Install Python Dependencies
```bash
# Navigate to your project
cd /root/Green-Repository

# Install packages
python3 -m pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings

# Or use the requirements file:
python3 -m pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (optional, has good defaults)
```

### 3. Start Server
```bash
bash start.sh
# Server will be at http://localhost:8000
```

## Testing Your Server

Once running, you can:

1. **View Interactive Docs**: http://localhost:8000/docs
2. **Try API Endpoints**: All endpoints have test buttons in the docs UI
3. **Send Test Data**: Use curl or Postman to send sensor readings
4. **Check Health**: http://localhost:8000/health

## Integration Points

### For Your IoT Devices
Send sensor readings to:
```
POST http://your-server:8000/api/v1/iot/sensor-reading
```

With JSON like:
```json
{
  "device_id": "camera_001",
  "timestamp": "2024-05-21T10:30:00",
  "latitude": 1.3521,
  "longitude": 103.8198,
  "sensor_type": "camera",
  "raw_data": {
    "frame_id": 123,
    "resolution": "1920x1080"
  }
}
```

### For Your Mobile App
Connect WebSocket to:
```
ws://your-server:8000/api/v1/stream/ws/live-detections
```

Or fetch recent detections:
```
GET http://your-server:8000/api/v1/stream/detections/recent
```

## AI/ML Integration

The AI detection is currently a **placeholder** with mock detections. To integrate your model:

1. **Option A: Pickle/Joblib Model**
   ```python
   # Put your model in models/detector.pkl
   # The system will automatically load it
   ```

2. **Option B: Custom Deep Learning**
   ```python
   # Edit app/ai/detector.py
   # Load your TensorFlow/PyTorch/YOLOv8 model
   # Replace the _mock_detection() method
   ```

3. **Example: YOLOv8 Integration**
   ```python
   from ultralytics import YOLO
   
   class DetectionModel:
       def __init__(self):
           self.model = YOLO('yolov8m.pt')  # Load YOLO model
       
       def predict(self, image):
           results = self.model(image)
           return [{
               "type": r.name,
               "confidence": float(r.conf),
               "box": r.xyxy.tolist()
           } for r in results]
   ```

## Database Setup

### For Development (SQLite)
- **No setup needed!** Database auto-creates at `green_repository.db`
- Perfect for testing and local development

### For Production (PostgreSQL)
```bash
# Start database with Docker
docker-compose up -d postgres

# Update .env
DATABASE_URL=postgresql://green_user:green_password@localhost:5432/green_repository

# Restart server
bash start.sh
```

## Deployment Checklist

- [ ] Replace mock AI detector with your trained model
- [ ] Update CORS settings in app/main.py for your domain
- [ ] Add forest zone definitions to database
- [ ] Configure alert thresholds in settings
- [ ] Set up PostgreSQL for production
- [ ] Add authentication/API keys
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure backups for database
- [ ] Deploy to cloud or on-premise server

## Files Reference

| File | Purpose |
|------|---------|
| `app/main.py` | Main FastAPI application |
| `app/models/sensor_data.py` | Input/output data schemas |
| `app/models/orm.py` | Database tables |
| `app/routes/iot.py` | IoT sensor endpoints |
| `app/routes/stream.py` | WebSocket & streaming |
| `app/routes/ai.py` | Detection endpoints |
| `app/ai/detector.py` | ML model & inference |
| `app/services/db.py` | Database connections |
| `.env.example` | Environment variables |
| `requirements.txt` | Python dependencies |
| `GETTING_STARTED.md` | Detailed guide |

## Useful Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [WebSocket Guide](https://fastapi.tiangolo.com/en/docs/advanced/websockets/)
- [YOLOv8 Detection](https://github.com/ultralytics/ultralytics)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

## Support & Questions

The project includes comprehensive documentation:
- **README.md** - Project overview
- **GETTING_STARTED.md** - Step-by-step setup guide
- **API Docs** - Available at `/docs` when running

## Next Steps

1. ✅ **Project structure complete**
2. → **Install dependencies** (requirements.txt)
3. → **Start server** (bash start.sh)
4. → **Train AI model** for illegal logging detection
5. → **Connect IoT devices** to sensor endpoints
6. → **Build mobile app** with WebSocket connection
7. → **Deploy to cloud** (AWS, GCP, Azure, etc.)

---

**Ready to run?**
```bash
cd /root/Green-Repository
python3 -m pip install -r requirements.txt
bash start.sh
```

Visit http://localhost:8000/docs to see all available endpoints! 🚀
