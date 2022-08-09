import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("./build-order-guide-firebase-adminsdk-goucp-24ed83eca1.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_data_to_db(data, game_name):
    data = json.loads(json.dumps(data))

    doc_ref = db.collection(u'matches').document(u'nOuk4lquYrXt4H2xafiZpPUFvN82').collection('data').document(game_name)
    doc_ref.set(data)