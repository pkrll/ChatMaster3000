import urwid
from core.ui.components.wrapper import Wrapper

class ChatWindow(urwid.ListBox, Wrapper):
    """
        A ListBox urwid widget representing the chat log of the application.

        All messages to the user will be displayed in the chat window.
        The ListBox's content will consist only of a list walker widget.
    """

    def __init__(self):
        body = urwid.SimpleFocusListWalker([])
        super(ChatWindow, self).__init__(body)
