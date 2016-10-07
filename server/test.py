from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import json

class CMServer(Protocol):
    username = None
    def connectionMade(self):
        self.factory.connections.append(self)
        print self.factory.connections
        self.makeRequest("login")

    def makeRequest(self, request):
        data = json.dumps({
        "type": "request",
        "data": {"request": request}
        })
        self.transport.write(data)

    def dataReceived(self, data):
        package = json.loads(data)
        if "data" not in package:
            return
        else:
            data = package["data"]

        if "type" in package:
            if package["type"] == "command":
                if data["command"] == "login":
                    username = data["parameters"]["username"]
                    if self.factory.isUserUnique(username):
                        self.username = username
                        self.sessionStarted()

    def sessionStarted(self):
        data = json.dumps({
        "type": "session",
        "data": {
            "status": 1
            }
        })
        self.transport.write(data)
        print data




class CMServerFactory(Factory):
    #Set the protocol to the server
    protocol = CMServer

    connections = []

    def isUserUnique(self, username):
        for conn in self.connections:
            if username == conn.username:
                return False
        return True

    def sendAll(self):
        for conn in self.connections:
            conn.transport.write("hej")



# 8007 is the port you want to run under. Choose something >1024
endpoint = TCP4ServerEndpoint(reactor, 9000)
endpoint.listen(CMServerFactory())
reactor.run()
