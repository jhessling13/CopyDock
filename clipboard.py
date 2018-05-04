# =================================================================================================
# Clipboard manager class
#
# Clipboard object with a stack of items.
# =================================================================================================
from clip import clip
import json


class clipboard:
    def __init__(self):
        self.__stack_index__ = -1
        self.__stack__ = []
        self.__current_item__ = None
        self.__cycle__ = False
        self.__comment_stack__ = []

    def getIndex(self):
        self.__stack_index__ = self.getStackSize() - 1
        return self.__stack_index__

    def getStackSize(self):
        return len(self.__stack__)

    def getCurrentItem(self):
        return self.__current_item__

    def isItemIn(self, item):
        i = 0
        for a in self.__stack__:
            if item == a.text:
                return self.getStackSize() - i
            i += 1
        return -1

    def _syncItem(self):
        self.__stack_index__ = self.getStackSize() - 1
        if self.__stack_index__ >= 0:
            self.__current_item__ = self.__stack__[self.__stack_index__]
        else:
            self.__current_item__ = None

    def _getItemAt(self, reqIndex):
        if self.__stack_index__ <= reqIndex >= 0:
            return self.__stack_index__
        else:
            return None

    def addItem(self, item, comment=""):
        self.__stack__.append(clip(item, comment))
        self._syncItem()

    def setComment(self, comment, index):
        if self.getStackSize() >= index >= 0:
            self.__stack__[index].setComment(comment)

    def popStack(self):
        if self.__stack_index__ >= 0:
            poppedItem = self.__stack__.pop()
            self._syncItem()
            return poppedItem
        return self.getCurrentItem()

    def softPop(self):
        if self.__stack_index__ >= 0:
            self.__stack__.insert(0, self.__stack__.pop())
            self._syncItem()
        return self.__current_item__

    def indexPop(self, index):
        if self.__stack_index__ >= index:
            poppedItem = self.__stack__.pop(index)
            self.__stack__.append(poppedItem)
            self._syncItem()
            return poppedItem
        return self.__current_item__

    def getComment(self, index=-1):
        if self.__stack_index__ >= index >= 0:
            return self.__stack__[index].comment

    def getStack(self):
        return self.__stack__

    def clearStack(self):
        self.__stack__ = []
        self.__stack_index__ = -1
        self._syncItem()

    def dumpToArchiveFile(self, filename="archive.txt"):
        with open(filename, "w") as archiveFileHandle:
            dictStack = []

            for a in self.__stack__:
                dictStack.append({'text': a.text, 'comment': a.comment})

            json.dump(dictStack, archiveFileHandle, indent=1)
