import firebase_admin
from firebase_admin import credentials
from django.conf import settings
import os

# Path to your service account key file
cred_path = os.path.join(settings.BASE_DIR, "firebase-admin-key.json")

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    app = firebase_admin.initialize_app(cred)  
else:
    app = firebase_admin.get_app()  
