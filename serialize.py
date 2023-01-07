def serializeConnectedClient(connectedClient):
    serializedConnectedClient = {}
    serializedConnectedClient["id"]= connectedClient.id
    serializedConnectedClient["sid"]= connectedClient.sid
    serializedConnectedClient["name"]= connectedClient.name
    serializedConnectedClient["ready"]= connectedClient.ready

def serializeConnectedClientList(connectedClientList):
    serializedConnectedClientList = []
    for connectedClient in connectedClientList:
        serializedConnectedClientList.append(
            serializeConnectedClient(connectedClient)
        )
    return serializedConnectedClientList