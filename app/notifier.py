#!/usr/bin/env python3
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VENV_DIR = os.path.join(REPO_ROOT, ".venv")

if os.path.isdir(VENV_DIR):
    for candidate in (
        os.path.join(VENV_DIR, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"),
        os.path.join(VENV_DIR, "Lib", "site-packages"),
    ):
        if os.path.isdir(candidate) and candidate not in sys.path:
            sys.path.insert(0, candidate)

import firebase_admin
from firebase_admin import credentials, messaging

SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
if not SERVICE_ACCOUNT_PATH:
    repo_candidate = os.path.join(
        REPO_ROOT,
        "app",
        "firebase.json",
    )
    SERVICE_ACCOUNT_PATH = repo_candidate if os.path.exists(repo_candidate) else "/opt/forest_alert_server/serviceAccountKey.json"

# Initialize Firebase Admin SDK lazily so tests and local usage can import the module.
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
    except Exception as exc:  # pragma: no cover - environment-specific
        print(f"[WARN] Firebase not initialized: {exc}")


def _normalize_location(location):
    if location is None:
        return "unknown"
    location_str = str(location).strip()
    if not location_str or location_str.lower() in {"n/a", "na", "none", "unknown"}:
        return "unknown"
    return location_str


def build_message(target_token=None, title="Hello", body="Test notification", data=None):
    payload = {
        "notification": messaging.Notification(title=title, body=body),
        "android": messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                channel_id="emergency_channel",
                sound="default",
                priority="high",
            ),
        ),
    }
    if data:
        payload["data"] = data

    if target_token:
        return messaging.Message(token=target_token, **payload)
    return messaging.Message(topic="forest_alerts", **payload)


def send_alert(incident_id, alert_type, location, target_token=None, device_id=None):
    """
    Sends a high-priority FCM notification to the Kotlin mobile app.
    If target_token is provided, sends to that device; otherwise sends to the topic.
    """
    normalized_location = _normalize_location(location)
    title = f"🚨 {alert_type.upper()} ALERT"
    body = f"{alert_type.title()} detected for device {device_id or 'unknown'}"
    if normalized_location != "unknown":
        body = f"{body} at {normalized_location}"

    message_args = {
        "notification": messaging.Notification(
            title=title,
            body=body,
        ),
        "data": {
            "incident_id": str(incident_id),
            "alert_type": alert_type,
            "location": normalized_location,
            "device_id": str(device_id or "unknown"),
        },
        "android": messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                channel_id="emergency_channel",
                sound="default",
                priority="high",
            ),
        ),
    }

    message = build_message(
        target_token=target_token,
        title=message_args["notification"].title,
        body=message_args["notification"].body,
        data=message_args["data"],
    )

    try:
        response = messaging.send(message)
        print(f"[SUCCESS] Dispatched notification for Incident {incident_id}: {response}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send notification: {e}")
        return False


def send_test_push(target_token=None, title="Hi", body="Hello from Green Server"):
    """Send a simple test notification for debugging."""
    if not target_token:
        target_token = os.getenv("FCM_DEVICE_TOKEN")
    if not target_token:
        print("[WARN] No FCM device token supplied. Set FCM_DEVICE_TOKEN or pass target_token.")
        return False

    message = build_message(target_token=target_token, title=title, body=body)
    try:
        response = messaging.send(message)
        print(f"[SUCCESS] Test notification sent: {response}")
        return True
    except Exception as exc:
        print(f"[ERROR] Test notification failed: {exc}")
        return False


if __name__ == "__main__":
    send_test_push(target_token=os.getenv("FCM_DEVICE_TOKEN"))