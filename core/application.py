import urwid
from twisted.internet import reactor
from core.client.chatclientfactory import ChatClientFactory
from core.ui.windowframe import WindowFrame
from support.const.globals import serverInformation, defaultPalette

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
    """

    user            = dict(username=None, id=None)
    isConnected     = False
    frame           = None
    mainLoop        = None
    clientFactory   = None

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
        self.frame.printToScreen("[ Error: %s]" % reason, "bold-heading")
        self.shouldUpdateScreen()
        self.isConnected = False

    def didFailConnection(self, reason):
        self.frame.printToScreen("[ Error: %s ]" % reason, "bold-heading")
        self.shouldUpdateScreen()
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
                        self.frame.printToScreen("[ Error: Not connected to the server. Use the /connect command. ]", "bold-heading")
                else:
                    text = "%s: %s" % (self.user["username"], parameter)
                    self.frame.printToScreen(text)
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
        self.frame.printToScreen("Welcome %s. Attempting to connect to the server..." % self.user["username"])
        reactor.connectTCP(serverInformation["addr"], serverInformation["port"], self.clientFactory)

    def __didReceiveCommand(self, command):
        """
            Invoked when the user inputs a /command.

            Args:
                command (str)   :   The command.
        """
        if len(command) > 0:
            # Turn to lower case and split its arguments
            command = command.lower().split(" ")
            if command[0] == "exit":
                raise urwid.ExitMainLoop()
            elif command[0] == "help":
                self.__showHelp()
            elif command[0] == "clear":
                self.frame.clearChatLog()
            else:
                self.frame.printToScreen("[ Error: command %s not found. ]" % (command[0]), "bold-heading")
        else:
            self.frame.printToScreen("[ Error: No command given. ]", "bold-heading")

    def __showHelp(self):
        text = "\n"
        text += "ChatMaster 3000 commands:\n\n"
        text += "/exit - quit the program\n"
        text += "/clear - clear the chat log\n"
        text += "/connect - connect to the server\n"
        text += "/rename - Change username\n\n"
        text += "/help - show this guide\n\n"
        self.frame.printToScreen(text)
