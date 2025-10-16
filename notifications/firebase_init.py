import os
import json
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase app only once
if not firebase_admin._apps:
    # Get the JSON string from environment variable
    firebase_creds = os.environ.get("FIREBASE_CREDENTIALS")

    if firebase_creds:
        cred_dict = json.loads(firebase_creds)  # parse JSON string
        cred = credentials.Certificate(cred_dict)
        app = firebase_admin.initialize_app(cred)
    else:
        raise Exception("FIREBASE_CREDENTIALS environment variable not set")
else:
    app = firebase_admin.get_app()
