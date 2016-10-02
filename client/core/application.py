import urwid, json, time
from twisted.internet import reactor
from core.client.chatclientfactory import ChatClientFactory
from core.ui.emptyframe import EmptyFrame
from core.ui.loginframe import LoginFrame
from core.ui.chatframe import ChatFrame
from support.const.globals import serverInformation, defaultPalette, availableCommands
from support.helpers import newMessage, newCommand

class Application(object):
    """
        The ChatMaster 3000 application.

        Acts as the controller of the application, acting as the middle man
        between the UI (view) and the chat protocol (model, sort of...).

        Args:
            isConnected (bool)      :   A boolean value indicating whether the user is connected.
            frame (obj)             :   The UI frame of the application.
            mainLoop (obj)          :   The event loop.
            clientFactory (obj)     :   The chat protocol factory.
            connector (obj)         :   A connector object.
            alamarHandler (tuple)   :   A handler for the urwid  alarm
    """

    isConnected     = False
    frame           = None
    mainLoop        = None
    clientFactory   = None
    connector       = None
    alarmHandler    = None

    def __init__(self):
        """
        """
        self.__preliminaries()
        self.mainLoop = urwid.MainLoop(EmptyFrame("Welcome to ChatMaster 3000", self), defaultPalette, event_loop=urwid.TwistedEventLoop())
        self.mainLoop.screen.set_terminal_properties(colors=256)

        self.__transitionToFrame(LoginFrame, 1)
        self.mainLoop.run()

    def didReceiveReturnKeyEvent(self, parameter=None):
        """
        """
        if parameter is None or not isinstance(parameter, basestring):
            return
        # If the login screen is visible
        # Can't use isinstance of here, because LoginFrame and ChatFrame
        # share the same base class.
        if str(self.frame.__class__) == str(LoginFrame):
            if self.isConnected is False:
                self.__makeConnection(parameter)
        else:
            if parameter.startswith("/"):
                self.__didReceiveCommand(parameter[1:])
            else:
                self.__sendMessage(parameter)
            self.frame.resetChatBox()

    def didReceiveArrowKeyEvent(self, parameter=None):
        pass

    def didConnect(self):
        self.isConnected = True
        self.__setFrame(EmptyFrame(["Connection established.", "Joining server..."]))
        time.sleep(1) # TODO: REMOVE ME

    def didJoinServer(self):
        self.__transitionToFrame(ChatFrame)
        self.frame.printToScreen("Successfully connected.", "bold-heading")
        self.shouldUpdateScreen()
        self.frame.enableChatBox(True)

    def didFailConnection(self, reason):
        self.isConnected = False
        self.__setFrame(EmptyFrame(["Connection failed.", "", reason], self))
        self.__transitionToFrame(LoginFrame, 2)

    def didLoseConnection(self, reason):
        self.isConnected = False
        self.__setFrame(EmptyFrame(["Connection lost.", "", reason], self))
        self.__transitionToFrame(LoginFrame, 2)

    def didReceiveMessage(self, message):
        self.frame.printToScreen(message)

    def shouldUpdateScreen(self):
        self.mainLoop.draw_screen()

    def shouldUpdateChannelList(self, channels):
        """
        """
        # Can't use isinstance because of shared superclass
        if str(self.frame.__class__) == str(ChatFrame):
            self.frame.setChannelList(channels)

    def shouldSkipTransitionTimer(self):
        """
        """
        if self.alarmHandler is not None:
            self.alarmHandler.func()
            self.mainLoop.remove_alarm(self.alarmHandler)
            self.alarmHandler = None

    ##########################
    #   Semi-private methods
    ##########################

    def __preliminaries(self):
        """
        """
        self.clientFactory = ChatClientFactory(self)

    def __makeConnection(self, username):
        """
            Attempts to connect to the server.
        """
        self.__setFrame(EmptyFrame(["Connecting..."]))
        time.sleep(1) # TODO: REMOVE ME
        self.clientFactory.setUsername(username)
        self.connector = reactor.connectTCP(serverInformation["addr"], serverInformation["port"], self.clientFactory)

    def __sendMessage(self, message):
        """
            Send a message to the server.

            Args:
                message (str)   :   The message to send.
        """
        if self.isConnected or self.connector is not None:
            package = newMessage(message)
            text = "%s: %s" % (self.clientFactory.username, message)
            self.frame.printToScreen(text)
            # TODO: The server must be able to know who writes what? Create packages?
            # or let the server keep track of the client connected...?
            self.connector.transport.write(package)
        else:
            self.frame.printErrorMessage("You must be connected.")

    #
    #   Frame Methods
    #

    def __transitionToFrame(self, newFrame, transitionInSeconds = 0):
        """
        """
        if transitionInSeconds > 0:
            def exitFrame(loop, user_data=None):
                self.__setFrame(newFrame(self))
            self.alarmHandler = self.mainLoop.set_alarm_in(transitionInSeconds, exitFrame)
        else:
            self.__setFrame(newFrame(self))

    def __setFrame(self, newFrame):
        """
            Sets the window frame.

            Note:
                This method also releases the last used frame.

            Args:
                newFrame (obj)  :   The new frame.
        """
        lastUsedFrame = self.mainLoop.widget.base_widget
        self.mainLoop.widget = newFrame
        self.frame = newFrame
        self.shouldUpdateScreen()

        del(lastUsedFrame) # Try to release it

    #
    #   Command Methods
    #

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
            self.frame.printErrorMessage("Command %s not found." % command[0])
        else:
            self.frame.printErrorMessage("No command given.")

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
            self.frame.printErrorMessage("Connection already established. Please use /disconnect first.")
        else:
            self.__makeConnection()

    def __executeCommandDisconnect(self, parameter=None):
        """
            Disconnect from the server.
        """
        if self.isConnected and self.connector is not None:
            self.connector.disconnect()
        else:
            self.frame.printErrorMessage("Not connected.")

    def __executeCommandRename(self, parameter=None):
        """
            Sets a new username.

            TODO: Let the server know of the name change. (Also, the server should announce it to all with a notification message)
        """
        if parameter is None and len(parameter) > 0:
            return

        # data = self.__createJSONPackage({
        #     "type": "command",
        #     "data": { "command": "rename", "parameter": parameter[0] }
        # })
        #
        # self.connector.transport.write(data)

    def __executeCommandHelp(self, parameter=None):
        text = "ChatMaster 3000 commands:\n"
        text += "/exit - quit the program\n"
        text += "/clear - clear the chat log\n"
        text += "/connect - connect to the server\n"
        text += "/disconnect - disconnect from the server\n"
        text += "/rename - Change username\n"
        text += "/help - show this guide"
        self.frame.printToScreen(text)
