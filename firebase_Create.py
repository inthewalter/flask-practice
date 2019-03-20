import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseCreate :
  def __init__(self) :
    cred = credentials.Certificate('./firebase-key.json')
    firebase_admin.initialize_app(cred)
    self.db = firestore.client()
    pass
  
  def upload(self, hakbu, notice_data) :
    self.db.collection(hakbu).document(notice_data['no']).set(notice_data)