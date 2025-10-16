from firebase_admin import messaging
from notifications.models import Notification
from .firebase_init import app  # ensure Firebase is initialized
from users.models import UserDevice  # import your UserDevice model


def send_firebase_notification(fcm_token, title, body, data=None):
    """
    Send a push notification via Firebase Cloud Messaging (FCM).
    """
    if not fcm_token:
        print("[FCM] ❌ No Firebase token provided — skipping notification.")
        return

    try:
        # Create FCM message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=fcm_token,
        )

        # Send message via Firebase Admin SDK
        response = messaging.send(message)
        print(f"✅ [FCM] Notification sent successfully. Response ID: {response}")

    except messaging.ApiCallError as e:
        print(f"⚠️ [FCM] API call failed: {e}")
    except Exception as e:
        print(f"❌ [FCM] Unexpected error sending notification: {e}")


def create_budget_notification(user, title, message, type="budget"):
    """
    Creates a Notification in the database and sends a Firebase push notification to all of the user's devices.
    """
    try:
        # Save to database
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            type=type
        )

        # Get all devices for this user
        devices = user.devices.all()  # related_name="devices" in UserDevice

        if not devices:
            print("[Notification] ⚠️ No devices found for user — skipping push.")
            return

        # Send FCM to each device
        for device in devices:
            send_firebase_notification(device.fcm_token, title, message)

    except Exception as e:
        print(f"[Notification Error] ❌ {e}")
