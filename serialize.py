def serializeConnectedClient(connectedClient):
    serializedConnectedClient = {}
    serializedConnectedClient["id"]= connectedClient[0]
    serializedConnectedClient["sid"]= connectedClient[1]
    serializedConnectedClient["name"]= connectedClient[2]
    serializedConnectedClient["ready"]= connectedClient[3]
    serializedConnectedClient["score"]= connectedClient[4]
    return serializedConnectedClient

def serializeConnectedClientList(connectedClientList):
    serializedConnectedClientList = []
    for connectedClient in connectedClientList:
        serializedConnectedClientList.append(
            serializeConnectedClient(connectedClient)
        )
    return serializedConnectedClientList