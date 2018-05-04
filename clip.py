# =================================================================================================
# Clip object class
#
# Represents a clip object, including the clip-text and comment.
# =================================================================================================
import time


class clip:
    def __init__(self, text, comment="(blank)", date=time.strftime("%Y%m%d%H%M%S")):
        self.text = text
        self.comment = comment
        self.date = date

    def __str__(self):
        return str(self.text) + " -> " + self.date + ": " + self.comment

    def setComment(self, comment):
        self.comment = comment

    def setText(self, text):
        self.text = text

    def setDate(self, date):
        self.date = date
