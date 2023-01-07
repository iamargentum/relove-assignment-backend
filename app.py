import sqlite3
from flask import Flask, request
from flask_socketio import SocketIO

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

operation = ""

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def clientConnected():
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"INSERT INTO connected_clients (sid, name, ready) VALUES ('{request.sid}', '', {False})")
        dbConn.commit()

@socketio.on("setName")
def setClientName(data):
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"UPDATE connected_clients SET name='{data}' WHERE sid='{request.sid}'")
        dbConn.commit()

@socketio.on("ready")
def clientReady():
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"UPDATE connected_clients SET ready={True} WHERE sid='{request.sid}'")
        dbConn.commit()

@socketio.on("disconnect")
def clientDisconnected():
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"DELETE FROM connected_clients where sid='{request.sid}'")
        dbConn.commit()

if __name__ == '__main__':
    socketio.run(app)