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
      return self.__stack_index__

   def getStackSize(self):
      return self.getIndex() + 1

   def getCurrentItem(self):
      return self.__current_item__

   def isItemIn(self, item):
      # return item in self.__stack__
      i = 0
      for a in self.__stack__:
         if item == a.text:
            return len(self.__stack__) - 1 - i
         i += 1
      return -1

   def toggleCycle(self, enabled):
      self.__cycle__ = enabled

   def _syncItem(self, indexMod=0):
      self.__stack_index__ += indexMod
      if self.__stack_index__ >= 0:
         self.__current_item__ = self.__stack__[self.__stack_index__]
      else:
         self.__current_item__ = None

   def _getItemAt(self, reqIndex):
      if reqIndex >= 0 and reqIndex <= self.__stack_index__:
         return self.__stack_index__
      else:
         return None

   def addItem(self, item, prepend=False):
      if prepend:
         self.__stack__.insert(0, clip(item))
         # self.__comment_stack__.insert(0, comment)
      else:
         self.__stack__.append(clip(item))
         # self.__comment_stack__.append((comment))
      self._syncItem(1)

   def addItemWithComment(self, item, comment, prepend=False):
      if prepend:
         self.__stack__.insert(0, clip(item, comment))
         # self.__comment_stack__.insert(0, comment)
      else:
         self.__stack__.append(clip(item, comment))
      self._syncItem(1)
      print("Added this in the clipboard - ", item, " >> ", comment)

   def setComment(self, comment, index):
      if index >= 0 and self.__stack_index__ >= index:
         self.__stack__[index].setComment(comment)
         # print("comment added: ", self.__stack__[index].comment, " << ", self.__stack__[index].text)

   def popStack(self):
      if self.__stack_index__ >= 0:
         poppedItem = self.__stack__.pop()
         if self.__cycle__:
            self.__stack__.insert(0, poppedItem)
            self._syncItem()
         else:
            self._syncItem(-1)
         return poppedItem
      return self.__current_item__

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
      if index >= 0 and self.__stack_index__ >= index:
         return self.__stack__[index].comment

   def getStack(self):
      return self.__stack__

   def clearStack(self):
      self.__stack__ = []
      self.__stack_index__ = -1
      self._syncItem()

   def dumpToArchiveFile(self, filename="archive.txt"):
      archiveFileHandle = open(filename, "w")
      dictStack = []

      for a in self.__stack__:
         dictStack.append({'text':a.text, 'comment':a.comment})

      json.dump(dictStack, archiveFileHandle, indent=1)
      archiveFileHandle.close()