from app import db

class ConnectedClient(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=True)
    ready = db.Column(db.Boolean, default=False)