"""FastAPI application entry point."""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db, init_db, User
from app.schemas import UserLogin, UserRegister, UserResponse

app = FastAPI(
    title="Green Repository",
    description="IoT Environmental Monitoring Server"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Green Repository",
        "status": "running",
        "timestamp": datetime.utcnow(),
        "update": "v3.0 - Added user registration and login endpoints"
    }


@app.get("/health")
async def health():
    """Health check."""
    print(f"[HEALTH CHECK] Status: healthy at {datetime.utcnow()}")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }


@app.post(
    "/register",
    response_model=UserResponse,
    responses={400: {"description": "Duplicate email"}},
)
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **username**: Username (3-50 characters)
    - **password**: Password (6-50 characters)
    - **email**: Email address
    - **phone**: Phone number (max 12 characters)
    """
    print(f"[REGISTER REQUEST] Received: username={user.username}, email={user.email}, phone={user.phone}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        print(f"[REGISTER RESPONSE] Duplicate email error: {user.email}")
        return JSONResponse(status_code=400, content={"error": "duplicateemail"})

    new_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
        phone=user.phone,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"[REGISTER RESPONSE] User registered successfully: id={new_user.id}, email={new_user.email}")
    return new_user


@app.post(
    "/login",
    response_model=UserResponse,
    responses={401: {"description": "Invalid credentials"}},
)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user by email and password.

    - **email**: Registered email address
    - **password**: User password
    """
    print(f"[LOGIN REQUEST] Received: email={user.email}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or existing_user.password != user.password:
        print(f"[LOGIN RESPONSE] Invalid credentials for: {user.email}")
        return JSONResponse(status_code=401, content={"error": "invalidcredentials"})

    print(f"[LOGIN RESPONSE] Login successful: id={existing_user.id}, email={existing_user.email}")
    return UserResponse(
        id=existing_user.id,
        username=existing_user.username,
        email=existing_user.email,
        phone=existing_user.phone,
        registered_date=existing_user.registered_date,
    )


@app.get("/dashboard")
async def get_dashboard_data():
    """
    Placeholder endpoint for dashboard data.
    You can customize this to return relevant information for your dashboard.
    """
    return {
        "message": "Welcome to the Green Repository Dashboard!",
        "status": "data_ready",
        "timestamp": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
