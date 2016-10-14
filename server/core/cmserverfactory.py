from twisted.internet.protocol import Factory
from core.cmserver import CMServer
import json

class CMServerFactory(Factory):
    """
        The server factory class is responsible for creating new
        server protocol instances for new incoming connections.

        Args:
            protocol    (obj)   :   The Server Protocol.
            connections (list)  :   A list of current connections
            channels    (list)  :   A list of current channels.
    """

    protocol    = CMServer
    connections = []
    channels    = []
    defaultChannels = ["general", "python"]

    def __init__(self):
        self.channels = self.defaultChannels[:]

    def addConnection(self, connection):
        """
            Add a connection to the connections list.

            Args:
                connection (obj) : A new connection.
        """
        self.connections.append(connection)

    def removeConnection(self, connection):
        """
            Remove a connection from the connections list.

            Args:
                connection (obj) : The connection to remove.
        """
        self.connections.remove(connection)

    def didJoinChannel(self, channel, username):
        """
            Called when a user joins a channel.

            Should check if channel exists in the channels list. If
            not, add it.
        """
        users = []
        if not channel in self.channels:
            self.channels.append(channel)
            users.append(username)
        else:
            for connection in self.connections:
                if connection.channel == channel:
                    users.append(connection.username)

        self.sendNotification("user_joined", channel, {"channel": channel, "username": username, "current_users": users})

    def didLeaveChannel(self, channel, username):
        """
            Called when a user leaves a channel.

            Should check if the channel is empty. If so, remove it
            from the channels list.
        """
        users = []
        for connection in self.connections:
            # Check if the channel is empty
            if connection.channel == channel:
                users.append(connection.username)
        if len(users) > 0:
            # Notify the users in the channel and send an updated users list
            self.sendNotification("user_left", channel, {"channel": channel, "username": username, "current_users": users})
        elif channel not in self.defaultChannels and channel in self.channels:
            # Remove the channel if no one is inside
            self.channels.remove(channel)

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
                return False
        return True

    def sendMessage(self, message, username, toChannel=None):
        """
            Send a message to the users in a specific channel.

            Note:
                Method should check the which channel the connections
                (i.e. protocol objects) are inside, and only send
                to the ones inside that channel.

                A None value should route the message to users in
                the general channel.

            Args:
                message (json)  :   The message to send.
                toChannel  (str):   The channel the message should
                                    be routed to.
        """
        users = self.connections
        for conn in users:
            if toChannel == conn.channel and username != conn.username:
                conn.sendMessage(message, username)

    def sendNotification(self, event_type, toChannel=None, parameters=[]):
        """
            Send a notification to users in a specific channel.

            Args:
                event_type (str):   The event type.
                username (str)  :   The user that triggered the notification
                toChannel  (str):   The channel the message should be routed to.
        """
        for conn in self.connections:
            if toChannel == conn.channel:
                conn.sendNotification(event_type, parameters)

    # TODO: Abstrahera mera. sendMessage och sendNotification har mycket gemensamt.
