import json
from twisted.internet import protocol
from support.helpers import newCommand

class ChatClient(protocol.Protocol):
    """
        The ChatMaster 3000 client protocol.

        The client protocol is responsible for handling the communication
        between the server and the user.

        Args:
            delegate (obj)  :   The delegate of the client.
    """

    delegate = None
    username = None

    def __init__(self, username=None, delegate=None):
        """
            Initializes the object and sets the delegate.

            Note:
                The delegate will be notified upon events.
        """
        self.username = username
        self.delegate = delegate

    def connectionMade(self):
        """
            Invoked when the client has successfully connected
            to the server.

            Will call the Application method didConnect().
        """
        if self.delegate is not None:
            self.delegate.didConnect()

    def connectionLost(self, reason):
        """
            Invoked when the client has lost connection
            to the server.

            Args:
                reason (obj) : A connectionDone object.
        """
        if self.delegate is not None:
            self.delegate.didLoseConnection(reason.getErrorMessage())

    def dataReceived(self, data):
        """
            Invoked when the client receives data from
            the server.

            Args:
                data (str) : The data received.
        """
        package = json.loads(data)
        if "type" not in package:
            return
        # Use the type attribute to find the right handler method
        methodName = package["type"].capitalize()
        methodCall = getattr(self, "_"+self.__class__.__name__+"__handle"+methodName, None)
        data = package.get("data", None)
        if methodCall is not None:
            methodCall(data)

    def __handleMessage(self, package=None):
        """
            Handles messages sent from other users.

            Args:
                package (dict)  :   The message.
        """
        if package is None:
            return

        text = "%s: %s" % (package["username"], package["message"])
        self.delegate.didReceiveMessage(text)

    def __handleRequest(self, package=None):
        """
            Handles requests from the server.

            Args:
                package (dict)  :   The message.
        """
        requestType = package["request"]
        response = None
        if requestType == "login":
            # On requests of type login, the client
            # should send back the username.
            response = newCommand("login", {"username": self.username})
        if response is not None:
            self.transport.write(response)

    def __handleSession(self, package=None):
        """
            Handles session messages.

            Args:
                package (dict) :    The message.
        """
        if package is None:
            return

        if package["status"] is True:
            self.delegate.didJoinServer()
            self.delegate.shouldUpdateChannelList(package["channels"])
        else:
            self.delegate.didFailConnection(package["reason"])

    def __handleNotification(self, package=None):
        """
            Handles notifications from the server.

            Args:
                package (dict) :    The message.
        """
        eventType = package["event_type"]
        notification = None

        if eventType == "channel_list":
            self.delegate.shouldUpdateChannelList(package["channels"])
        elif eventType == "user_joined":
            notification = "User %s has joined the room." % package["username"]
        elif eventType == "user_left":
            notification = "User %s left the room." % package["username"]
        elif eventType == "user_rename":
            notification = "User %s changed nickname to %s" % (package["old_username"], package["new_username"])

        if notification is not None:
            self.delegate.didReceiveNotification(notification)

    def __handleError(self, package):
        """
            Handles errors from the server
        """
        pass
