
__author__ = "Peter Wolf"
__mail__ = "pwolf2310@gmail.com"
__date__ = "2016-12-25"

class Tag:

    """ Tag for an pr0gramm Item"""

    def __init__(self, id, confidence=None, tag=None):
        self.id = id
        self.confidence = confidence
        self.tag = tag


    def getText(self):
        return self.tag.encode("utf8")

    def getConfidence(self):
        return self.confidence

    def __str__(self):
        return self.getText()
