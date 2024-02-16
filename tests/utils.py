from __future__ import annotations

from html.parser import HTMLParser


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.anchors.append(attrs[0][1])


def count_anchors(html: str) -> int:
    parser = AnchorParser()
    parser.feed(html)
    return len(parser.anchors)
