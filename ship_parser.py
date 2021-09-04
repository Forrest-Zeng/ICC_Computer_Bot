from html.parser import HTMLParser
from discord.utils import escape_markdown as escape
class ShipParser(HTMLParser):
    def __init__(self):
        self.names = []
        self.finding = True
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "name_heading") in attrs:
            self.finding = True

    def handle_data(self, data):
        if self.finding == True and not data == "WHY?":
            self.names.append(escape(data.strip()))
            self.finding = False
