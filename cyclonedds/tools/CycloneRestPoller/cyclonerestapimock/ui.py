import urwid


palette = [
    ("headings", "light cyan", ""),
    ("bold", "bold", ""),
    ("body", "white", "")
]


class NodeWidget():
    def __init__(self, heading):
        self.heading = heading
        self.text = []

    def create_widget(self, api):
        if self.heading == "Node 1's opinion of Node 1":
            for method in api.call_local():
                self.text.append(("bold", f"{method.__class__.__name__}:\n  "))
                self.text.append(("body", f"{method}\n\n"))
        else:
            for method in api.call_remote():
                self.text.append(("bold", f"{method.__class__.__name__}:\n  "))
                self.text.append(("body", f"{method}\n\n"))
        linebox = self.draw_widget()
        return linebox

    def draw_widget(self):
        heading = urwid.AttrWrap(urwid.Text(self.heading, align="center"), "headings")
        listbox = urwid.ListBox(urwid.SimpleListWalker([urwid.Padding(urwid.Text(self.text), right=1)]))
        linebox = urwid.LineBox(urwid.Frame(urwid.AttrWrap(listbox, "body"), header=heading))
        return linebox
