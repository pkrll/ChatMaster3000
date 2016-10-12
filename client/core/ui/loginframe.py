import urwid
from core.ui.basicframe import BasicFrame
from core.ui.components.textfield import TextField
from support.clock import Clock

class LoginFrame(BasicFrame):
    """
        The login screen.

        TODO: The object is not properly released. Needs fixing.
    """

    def __init__(self, delegate, label="Type in your username:"):
        self.delegate = delegate
        label = urwid.Text(('bold-heading', label), align="center")
        field = TextField("", delegate=self, align="center")
        pile = urwid.Pile([label, field])
        body = urwid.AttrMap(urwid.Filler(pile), "background")

        header = urwid.AttrMap(urwid.Text(("bold-heading", "ChatMaster 3000"), align="center"), "background")
        footer = urwid.AttrMap(Clock(self, align="right"), "background")
        super(LoginFrame, self).__init__(body, header=header, footer=footer, focus_part='body')

    def didReceiveReturnKeyEvent(self, parameter=None):
        """
            Called from the subwidgets. Invoked when the
            user presses the return key.

            Args:
                parameter (Any) :   Some parameter.
        """
        # The parameter should be the text inside of the textbox
        # Check for content and call the delegate.
        if parameter is not None and len(parameter) > 0:
            self.delegate.didReceiveReturnKeyEvent(parameter)

    def shouldUpdateScreen(self):
        self.delegate.shouldUpdateScreen()
