from flask import Flask, request
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from serialize import serializeConnectedClient, serializeConnectedClientList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mathApp.db"
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)

OPERATION_CHOICES = [
    "ADD",
    "SUB",
    "MUL",
    "DIV"
]

operands = {
    "first": 0,
    "second": 0
}

operation = []

with app.app_context():
    db.create_all()

@socketio.on("connect")
def clientConnected():
    from models import ConnectedClient
    print("request is ", request.sid)
    connectedClient = ConnectedClient(
        sid=request.sid,
        name=""
    )
    db.session.add(connectedClient)
    db.session.commit()


@socketio.on("setName")
def setClientName(data):
    from models import ConnectedClient
    connectedClient = ConnectedClient.query.filter_by(sid=request.sid).first()
    connectedClient.name = data
    db.session.commit()
    connectedClientList = ConnectedClient.query.all()
    socketio.emit("updateUsersList", serializeConnectedClientList(connectedClientList), broadcast=True)

@socketio.on("ready")
def setClientName():
    from models import ConnectedClient
    connectedClient = ConnectedClient.query.filter_by(sid=request.sid).first()
    connectedClient.ready = True
    db.session.commit()
    db.session.refresh(connectedClient)
    clientsNotReady = ConnectedClient.query.filter_by(ready=False).all()
    print("clients that are not ready - ", clientsNotReady)

@socketio.on("disconnect")
def disconnect():
    print("disconnect triggered")
    print("request.sid is ", request.sid)
    from models import ConnectedClient
    db.session.execute('DELETE FROM connected_client WHERE sid = :val', {'val': request.sid})
    db.session.commit()
    connectedClientList = ConnectedClient.query.all()
    socketio.emit("updateUsersList", serializeConnectedClientList(connectedClientList), broadcast=True)

@socketio.on("submitAnswer")
def userSubmitted(data):
    pass


if __name__ == "__main__":
    socketio.run(app, debug=True)