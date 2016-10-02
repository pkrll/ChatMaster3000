import urwid

class EmptyFrame(urwid.AttrMap):

    delegate = None

    def __init__(self, label=None, delegate=None):
        self.delegate = delegate

        pile = urwid.Pile([])
        if isinstance(label, list):
            for item in label:
                element = urwid.Text(('bold-heading', item), align="center")
                pile.contents.append((element, pile.options()))
        else:
            if label is not None:
                label = urwid.Text(('bold-heading', label), align="center")
                pile.contents.append((label, pile.options()))

        filler = urwid.Filler(pile, 'middle')

        super(EmptyFrame, self).__init__(filler, "background")

    def keypress(self, size, key):
        if self.delegate is not None:
            self.delegate.shouldSkipTransitionTimer()
        return None

    def selectable(self):
        return True
