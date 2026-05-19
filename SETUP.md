# Python server setup (FastAPI)

Prerequisites
- Python 3.10+ installed

Create virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run locally:

```bash
chmod +x start.sh
./start.sh
```

Open http://localhost:8000 for the API root and http://localhost:8000/docs for interactive docs.
