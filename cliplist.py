from dock import dock, textClip
from tkinter import *
from tkinter import ttk
import json

class cliplist(dock, Listbox):
   def __init__(self, topFrame, scrollbar):
      dock.__init__(self)
      self.cliplist = Scrollbar(topFrame)
      Listbox.__init__(self, topFrame, yscrollcommand=scrollbar.set, selectmode=SINGLE)

   def addItem(self, item, comment=""):
      dock.addTextClip(self, item, comment)
      Listbox.insert(self, 0, item.replace("\n", "\\n"))
      self._setColors()

   def popStack(self):
      dock.hardPop(self)
      listpop = Listbox.get(self, 0)
      Listbox.delete(self, 0)
      self._setColors()
      return listpop

   def softPop(self):
      dock.softPop(self)
      listpop = Listbox.get(self, 0)
      Listbox.delete(self, 0)
      if len(listpop) > 0:
         Listbox.insert(self, END, listpop)
         self._setColors()
         return listpop
      return None

   def activePop(self):
      listLength = len(Listbox.get(self, 0, END))
      index = Listbox.index(self, ACTIVE)
      altIndex = (listLength - 1) - index
      dock.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   def indexPop(self, index):
      listLength = len(Listbox.get(self, 0, END))
      altIndex = (listLength - 1) - index
      dock.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   def clearStack(self):
      dock.clearDock(self)
      Listbox.delete(self, 0, END)

   # loop through listbox items and set the off-set colors and static highlight color
   def _setColors(self):
      listLength = len(Listbox.get(self, 0, END))
      for a in range(0, listLength):
         if a % 2 == 0:
            Listbox.itemconfig(self, a, bg='white smoke', selectbackground='SlateGray1', selectforeground='black')
         else:
            Listbox.itemconfig(self,a, bg='gainsboro', selectbackground='SlateGray1', selectforeground='black')