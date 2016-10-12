from twisted.internet.protocol import Protocol
import json

class CMServer(Protocol):
    """
        The server protocol handles each new incoming connection.

        Args:
            username (str)  :   The username.
            room     (str)  :   The room the client is currently in.
    """

    username = None
    room = None

    def __init__(self):
        pass

    def connectionMade(self):
        """
            Invoked when a new connection has been made.

            All new connections must be added to the factory, through
            the factory method addConnection().
        """
        self.factory.addConnection(self)
        self.sendRequest("login")

    def connectionLost(self, reason):
        """
            Invoked when a connection has been lost.

            Must call the factory method removeConnection().
        """
        self.factory.removeConnection(self)
        # TODO: Should send out a notification that the user has disconnected.

    def dataReceived(self, data):
        """
            Received data.

            This method checks and parses the data received. The
            data can be either a message or a command package.

            Messages should be rerouted to the right room, with the
            server factory method sendMessage(message, inRoom).

            Commands should be handled appropriately. See PROTOCOL.md
            for available commands.

            Args:
                data (json) : The data received.
        """
        data = json.loads(data)
        if data["type"] == "command":
            if data["data"]["command"] == "login":
                username = data["data"]["parameters"]["username"]
                nameUnique = self.factory.isUsernameUnique(username)
                if nameUnique:
                    self.sendSession(nameUnique)
                    self.username = username
                    self.factory.sendNotification("user_joined", username)
                else:
                    self.sendSession(nameUnique, "Username is already taken")
            # TODO: Add more commands
        elif data["type"] == "message":
            message = data["data"]["message"]
            self.factory.sendMessage(message,self.username,  self.room)

        # TODO: Add more package types


    def sendRequest(self, request):
        """
            Creates and sends a request message.

            Args:
                request (str) : The request to send.
        """
        data = json.dumps({
        "type": "request",
        "data": {"request": request}
        })
        self.transport.write(data)

    def sendSession(self, status, reason=None):
        """
            Send a session message.

            The session message indicates whether the client has
            successfully joined the server or not.

            The data attribute of a session message consists of two
            sub attributes:

                * status (with a boolean value),
                * reason (on failure) OR channels (on success)

            On success, the status attribute should be set to true,
            and the channels attribute consist of a list of public
            rooms.

            On failure, the status attribute should be set to false,
            with a reason string.

            Args:
                The status
        """
        data = None
        if status is True:
            # Create session package
            # and retrieve channels list through appropriate factory method.
            rooms = self.factory.rooms
            data = json.dumps({
            "type": "session",
            "data": {
            "status": status,
            "channels": rooms
            }
            })
        else:
            # Create session package
            # don't forget reason string
            data = json.dumps({
            "type": "session",
            "data": {
            "status": status,
            "reason": reason
            }
            })

        self.transport.write(data)

        # Don't forget to send it!
