import json

class textClip:
   def __init__(self, text, comment=""):
      self.text = text
      self.comment = comment

   def setComment(self, comment):
      self.comment = comment

   def setText(self, text):
      self.text = text

class dock:
   def __init__(self):
      self.__stack__ = []

   def size(self):
      return len(self.__stack__)

   def peek(self):
      return self.__stack__[len(self.__stack__) - 1]

   def addTextClip(self, text, comment=""):
      self.__stack__.append(clip(text, comment))

   def hardPop(self):
      return self.__stack__.pop()

   def softPop(self):
      x = self.__stack__.pop()
      self.__stack__.insert(0, x)
      return self.peek()

   def indexPop(self, index):
      x = self.__stack__.pop(index)
      self.__stack__.append(x)
      return self.peek()

   def indexDelete(self, index):
      return self.__stack__.pop(index)

   def clearDock(self):
      self.__stack__ = []

   def dumpToArchiveFile(self, filename="archive.txt"):
      with archiveFileHandle as open(filename, "w"):
         dictStack = []

         for a in self.__stack__:
            dictStack.append({'text':a.text, 'comment':a.comment})

         json.dump(dictStack, archiveFileHandle, indent=1)
