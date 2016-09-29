import urwid

class Wrapper(object):

    def wrapWithAttribute(self, attr):
        """
            Wraps the widget to the specified display attribute.

            The wrapper will apply the color as specified by the
            display attribute.

            Args:
                attr (str)  :   The identifier of the attribute.

            Returns:
                An urwid decoration widget.
        """
        return urwid.AttrMap(self, attr)
