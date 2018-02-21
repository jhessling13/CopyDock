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
      if not self.isEmpty():
         return self.__stack__[len(self.__stack__) - 1]
      else:
         return None

   def addTextClip(self, text, comment=""):
      self.__stack__.append(textClip(text, comment))

   def getClipText(self, index):
      if index >= 0 and self.size() - 1 >= index:
         return self.__stack__[index].text

   def setComment(self, comment, index):
      if index >= 0 and self.size() - 1 >= index:
         self.__stack__[index].setComment(comment)
   
   def getComment(self, index=-1):
      if index >= 0 and self.size() - 1 >= index:
         return self.__stack__[index].comment

   def hardPop(self):
      if not self.isEmpty():
         return self.__stack__.pop()
      else:
         return None

   def softPop(self):
      if not self.isEmpty():
         x = self.__stack__.pop()
         self.__stack__.insert(0, x)
         return self.peek()
      else:
         return None

   def indexPop(self, index):
      if not self.isEmpty():
         x = self.__stack__.pop(index)
         self.__stack__.append(x)
         return self.peek()
      else:
         return None

   def indexDelete(self, index):
      return self.__stack__.pop(index)

   def clearDock(self):
      self.__stack__ = []

   def isEmpty(self):
      return self.size() <= 0

   def isItemIn(self, item):
      i = 0
      for a in self.__stack__:
         if item == a.text:
            return self.size() - i
         i += 1
      return -1

   def dumpToArchiveFile(self, filename="archive.txt"):
      with open(filename, "w") as archiveFileHandle:
         dictStack = []

         for a in self.__stack__:
            dictStack.append({'text':a.text, 'comment':a.comment})

         json.dump(dictStack, archiveFileHandle, indent=1)
