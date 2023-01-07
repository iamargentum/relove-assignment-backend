import sqlite3
from flask import Flask, request
from flask_socketio import SocketIO
from utils import createQuestionAndGetAnswer
from serialize import serializeConnectedClientList, serializeConnectedClient

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

currentAnswer = 0

submittedAnswers = []

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
        result = cursor.execute(f"SELECT * FROM connected_clients")
        result = result.fetchall()
        listOfConnectedClients = serializeConnectedClientList(result)
        socketio.emit("updateUsersList", listOfConnectedClients)

@socketio.on("ready")
def clientReady():
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"UPDATE connected_clients SET ready={True} WHERE sid='{request.sid}'")
        dbConn.commit()
        result = cursor.execute(f"SELECT * FROM connected_clients")
        result = result.fetchall()
        listOfConnectedClients = serializeConnectedClientList(result)
        socketio.emit("updateUsersList", listOfConnectedClients)
        numClients = len(listOfConnectedClients)
        count = 0
        for client in listOfConnectedClients:
            if client["ready"]:
                count += 1
        if count == numClients:
            global currentAnswer
            operandsAndAnswer = createQuestionAndGetAnswer(OPERATION_CHOICES)
            operands["first"] = operandsAndAnswer["firstOperand"]
            operands["second"] = operandsAndAnswer["secondOperand"]
            currentAnswer = operandsAndAnswer["solution"]
            socketio.emit("newQuestion", {
                "operands": operands,
                "operation": operandsAndAnswer["operation"]
            })

@socketio.on("disconnect")
def clientDisconnected():
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"DELETE FROM connected_clients where sid='{request.sid}'")
        dbConn.commit()

@socketio.on("submitAnswer")
def answerSubmitted(data):
    global submittedAnswers
    print("data is ", data)
    print("sent by sid", request.sid)
    data["sid"] = request.sid
    submittedAnswers.append(data)
    with sqlite3.connect("mathApp.db") as dbConn:
        cursor = dbConn.cursor()
        cursor.execute(f"UPDATE connected_clients SET ready={True} WHERE sid='{request.sid}'")
        dbConn.commit()
        result = cursor.execute(f"SELECT * FROM connected_clients")
        result = result.fetchall()
        listOfConnectedClients = serializeConnectedClientList(result)
        if len(listOfConnectedClients) == len(submittedAnswers):
            print("inside list of clients is equal to submitted answers")
            fastestAnswerIndex = 0
            leastTime = submittedAnswers[0]["time"]
            for i in range(1, len(submittedAnswers)):
                answer = submittedAnswers[i]
                if answer["time"] < leastTime:
                    fastestAnswerIndex = i
            winnerSid = submittedAnswers[fastestAnswerIndex]["sid"]
            result = cursor.execute(f"SELECT * FROM connected_clients WHERE sid='{winnerSid}'")
            result = result.fetchone()
            winner = serializeConnectedClient(result)

            print("winner is ", winner)

            global operands
            global operation
            global currentAnswer
            
            operands = {
                "first": 0,
                "second": 0
            }
            operation = ""
            currentAnswer = 0
            submittedAnswers = []

            cursor.execute("UPDATE connected_clients SET ready=false")

            socketio.emit("winner", winner)

if __name__ == '__main__':
    socketio.run(app)