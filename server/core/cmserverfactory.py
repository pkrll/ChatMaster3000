from twisted.internet.protocol import Factory
from core.cmserver import CMServer

class CMServerFactory(Factory):
    """
        The server factory class is responsible for creating new
        server protocol instances for new incoming connections.

        Args:
            protocol    (obj)   :   The Server Protocol.
            connections (list)  :   A list of current connections
    """

    protocol    = CMServer
    connections = []
    rooms       = []

    def __init__(self):
        pass

    def addConnection(self, connection):
        """
            Add a connection to the connections list.

            Args:
                connection (obj) : A new connection.
        """
        connections.append(connection)

    def removeConnection(self, connection):
        """
            Remove a connection from the connections list.

            Args:
                connection (obj) : The connection to remove.
        """
        self.connections.remove(connection)

    def getRooms(self):
        pass

    def isUsernameUnique(self, username):
        """
            Check if the username is unique.

            Note:
                The server should allow only unique usernames.

            Args:
                username (str)  :   The username to check.

            Returns:
                A boolean indicating whether the username is
                already in use or not.
        """
        for conn in self.connections:
            if username == conn.username:
                return false
            else:
                return true

    def sendMessage(self, message, inRoom=None):
        """
            Send a message to the users in a specific room.

            Note:
                Method should check the which room the connections
                (i.e. protocol objects) are inside, and only send
                to the ones inside that room.

                A None value should route the message to users in
                the general room.

            Args:
                message (json)  :   The message to send.
                inRoom  (str)   :   The room the message should be
                                    routed to.
        """
        pass

    def sendNotification(self, inRoom=None):
        """
            Send a notification to users in a specific room.
        """
        pass
