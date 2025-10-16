from firebase_admin import messaging
from notifications.models import Notification
from .firebase_init import app  # ensure Firebase is initialized


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
    Creates a Notification in the database and sends a Firebase push notification to the user's device.
    """
    try:
        # Save to database
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            type=type
        )

        # Get user's FCM token
        fcm_token = getattr(user, "firebase_notification_token", None)

        if fcm_token:
            send_firebase_notification(fcm_token, title, message)
        else:
            print("[Notification] ⚠️ No Firebase token found for user — skipping push.")

    except Exception as e:
        print(f"[Notification Error] ❌ {e}")
