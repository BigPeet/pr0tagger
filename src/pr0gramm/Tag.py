
__author__ = "Peter Wolf"
__mail__ = "pwolf2310@gmail.com"
__date__ = "2016-12-25"

class Tag:

    """ Tag for an pr0gramm Item"""

    def __init__(self, id, confidence=None, text=None):
        self.id = id
        self.confidence = confidence
        self.text = text


    def getText(self):
        return self.text.encode("utf8")

    def __str__(self):
        return self.getText()
