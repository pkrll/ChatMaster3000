import urwid
from twisted.internet import reactor
from core.client.chatclientfactory import ChatClientFactory
from core.ui.windowframe import WindowFrame
from support.const.globals import serverInformation, defaultPalette, availableCommands

class Application(object):
    """
        The ChatMaster 3000 application.

        Acts as the controller of the application, acting as the middle man
        between the UI (view) and the chat protocol (model, sort of...).

        Args:
            user (dict)         :   A dictionary consisting of the user's information.
            isConnected (bool)  :   A boolean value indicating whether the user is connected.
            frame (obj)         :   The UI frame of the application.
            mainLoop (obj)      :   The event loop.
            clientFactory (obj) :   The chat protocol factory.
            connector (obj)     :   A connector object.
    """

    user            = dict(username=None, id=None)
    isConnected     = False
    frame           = None
    mainLoop        = None
    clientFactory   = None
    connector       = None

    def __init__(self):
        """
            Initializes the application and starts the event loop.

            Note:
                Before anything else, the __preliminaries() method will be called,
                setting up the client factory and the frame.
        """
        self.__preliminaries()
        self.__beginLoginProcess()
        self.mainLoop = urwid.MainLoop(self.frame, defaultPalette, event_loop=urwid.TwistedEventLoop())
        self.mainLoop.run()

    ##########################
    #   Event methods
    ##########################

    def didConnect(self):
        """
            Invoked when the client has established a connection.
        """
        self.isConnected = True
        self.frame.clearChatLog()
        self.frame.printToScreen("Successfully connected.", "bold-heading")
        self.shouldUpdateScreen()
        self.frame.enableChatBox(True)

    def didLoseConnection(self, reason):
        self.__printError(reason)
        self.isConnected = False

    def didFailConnection(self, reason):
        self.__printError(reason)
        self.frame.enableChatBox(True)

    def didReceiveReturnKeyEvent(self, parameter=None):
        """
            Reacts on return key events.

            Invoked when the return key has been pressed.

            Args:
                parameter (str) :   The parameter sent along from the sending object.
                                    In most cases, the sending object will be the chat
                                    box, sending the user inputed string.
        """
        if parameter is None:
            return

        if isinstance(parameter, basestring):
            if parameter.startswith("/"):
                self.__didReceiveCommand(parameter[1:])
            else:
                if self.isConnected is False:
                    if self.user["username"] == None:
                        self.user["username"] = parameter
                        self.__makeConnection()
                    else:
                        self.__printError("Not connected to the server. Use the /connect or /help command.")
                else:
                    self.__sendMessage(parameter)
            self.frame.resetChatBox()

    def didReceiveArrowKeyEvent(self, parameter=None):
        pass

    def shouldUpdateScreen(self):
        self.mainLoop.draw_screen()

    ##########################
    #   Semi-private methods
    ##########################

    def __preliminaries(self):
        """
            Sets up the client factory and the frame.
        """
        self.clientFactory = ChatClientFactory(self)
        self.frame = WindowFrame(self)

    def __beginLoginProcess(self):
        """
            Begins the connection process where the user will be
            asked to input username.
        """
        self.frame.printToScreen("Please enter your username...", "bold-heading")
        self.frame.setChatBoxCaption("Username: ")
        self.frame.enableChatBox(True)

    def __makeConnection(self):
        """
            Attempts to connect to the server.
        """
        self.frame.enableChatBox(False)
        self.frame.setChatBoxCaption("> ")
        self.frame.clearChatLog()
        self.frame.printToScreen("Attempting to connect to the server...")
        self.connector = reactor.connectTCP(serverInformation["addr"], serverInformation["port"], self.clientFactory)

    def __sendMessage(self, message):
        """
            Send a message to the server.

            Args:
                message (str)   :   The message to send.
        """
        if self.isConnected or self.connector is not None:
            text = "%s: %s" % (self.user["username"], message)
            self.frame.printToScreen(text)
            # TODO: The server must be able to know who writes what? Create packages?
            # or let the server keep track of the client connected...?
            self.connector.transport.write(message)
        else:
            self.__printError("You must be connected.")

    def __didReceiveCommand(self, command):
        """
            Invoked when the user inputs a /command.

            Args:
                command (str)   :   The command.
        """
        if len(command) > 0:
            # Turn to lower case and split its arguments
            command = command.lower().split(" ")
            if command[0] in availableCommands:
                methodName = "__executeCommand" + command[0].capitalize()
                # Must add the ugly prefix of _className because of the so called "private" accessor.
                methodCall = getattr(self, "_"+self.__class__.__name__+methodName, None)
                if methodCall is not None:
                    methodCall(command[1:])
                    return
            self.__printError("Command %s not found." % command[0])
        else:
            self.__printError("No command given.")

    def __printError(self, errorMessage, style="bold-heading"):
        """
            Print out an error message.

            Args:
                errorMessage (str)  : The error message to display.
                style (str)         : The style.
        """
        self.frame.printToScreen("[ Error: %s]" % errorMessage, style)
        self.shouldUpdateScreen()

    def __executeCommandExit(self, parameter=None):
        """
            Quit the application.
        """
        raise urwid.ExitMainLoop()

    def __executeCommandClear(self, parameter=None):
        """
            Clear the chat log.
        """
        self.frame.clearChatLog()

    def __executeCommandConnect(self, parameter=None):
        """
            Connect to the server.

            If already connected, alert the user.
        """
        if self.isConnected:
            self.__printError("Connection already established. Please use /disconnect first.")
        else:
            self.__makeConnection()

    def __executeCommandDisconnect(self, parameter=None):
        """
            Disconnect from the server.
        """
        if self.isConnected and self.connector is not None:
            self.connector.disconnect()
        else:
            self.__printError("Not connected.")


    def __executeCommandRename(self, parameter=None):
        """
            Sets a new username.

            TODO: Let the server know of the name change. (Also, it should announce it)
        """
        pass

    def __executeCommandHelp(self, parameter=None):
        text = "\n"
        text += "ChatMaster 3000 commands:\n\n"
        text += "/exit - quit the program\n"
        text += "/clear - clear the chat log\n"
        text += "/connect - connect to the server\n"
        text += "/disconnect - disconnect from the server\n"
        text += "/rename - Change username\n\n"
        text += "/help - show this guide\n"
        self.frame.printToScreen(text)
