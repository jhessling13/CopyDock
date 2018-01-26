# =================================================================================================
#
# Clip List
#
# Love-child of text-based clipboard class and tkinter Listbox class
# 
# Some ugly code below, could use some refactoring.
# =================================================================================================
from clipboard_b import clipboard
from tkinter import *
from tkinter import ttk
import json

class cliplist(clipboard, Listbox):
   def __init__(self, topFrame, scrollbar):
      clipboard.__init__(self)
      self.cliplist = Scrollbar(topFrame)
      Listbox.__init__(self, topFrame, yscrollcommand=scrollbar.set, selectmode=SINGLE)
      # self.comment = "(blank)"
      # Listbox.pack(topFrame, expand=True, fill='both')

   #extend clipboard class function to Listbox element...
   def addItem(self, item, prepend=False):
      clipboard.addItem(self, item, prepend)
      if prepend:
         Listbox.insert(self, END, item.replace("\n", "\\n"))
      else:
         Listbox.insert(self, 0, item.replace("\n", "\\n"))
      self._setColors()

   def addItemWithComment(self, item, comment="Blank", prepend=False):
      clipboard.addItemWithComment(self, item, comment, prepend)
      if prepend:
         Listbox.insert(self, END, item.replace("\n", "\\n"))
      else:
         Listbox.insert(self, 0, item.replace("\n", "\\n"))
      self._setColors()
      print("Added this: ", item)

   #extend clipboard class function to Listbox element...
   def popStack(self):
      clipboard.popStack(self)
      listpop = Listbox.get(self, 0)
      Listbox.delete(self, 0)
      self._setColors()
      return listpop

   #extend clipboard class function to Listbox element...
   def softPop(self):
      clipboard.softPop(self)
      listpop = Listbox.get(self, 0)
      Listbox.delete(self, 0)
      if len(listpop) > 0:
         Listbox.insert(self, END, listpop)
         self._setColors()
         return listpop
      return None

   #extend clipboard class function to Listbox element...
   def activePop(self):
      listLength = len(Listbox.get(self, 0, END))
      index = Listbox.index(self, ACTIVE)
      altIndex = (listLength - 1) - index
      clipboard.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   def indexPop(self, index):
      listLength = len(Listbox.get(self, 0, END))
      # index = Listbox.index(self, ACTIVE)
      altIndex = (listLength - 1) - index
      clipboard.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   #extend clipboard class function to Listbox element...
   def clearStack(self):
      clipboard.clearStack(self)
      Listbox.delete(self, 0, END)

   # loop through listbox items and set the off-set colors and static highlight color
   # todo: consider setting colors once, and updating text in Listbox items instead.
   #       would require changes to pop, add, and clear functions.  (set directly) vs. (StrinVar())?
   def _setColors(self):
      listLength = len(Listbox.get(self, 0, END))
      for a in range(0, listLength):
         if a % 2 == 0:
            Listbox.itemconfig(self, a, bg='white smoke', selectbackground='SlateGray1', selectforeground='black')
         else:
            Listbox.itemconfig(self,a, bg='gainsboro', selectbackground='SlateGray1', selectforeground='black')