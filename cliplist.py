# =================================================================================================
#
# Clip List
#
# Love-child of text-based clipboard class and tkinter Listbox class
# 
# Some ugly code below, could use some refactoring.
# =================================================================================================
from dock import dock, textClip
from tkinter import *
from tkinter import ttk
import json

class cliplist(dock, Listbox):
   def __init__(self, topFrame, scrollbar):
      dock.__init__(self)
      self.cliplist = Scrollbar(topFrame)
      Listbox.__init__(self, topFrame, yscrollcommand=scrollbar.set, selectmode=SINGLE)
      # self.comment = "(blank)"
      # Listbox.pack(topFrame, expand=True, fill='both')

   #extend clipboard class function to Listbox element...
   def addItem(self, item, comment=""):
      dock.addTextClip(self, item, comment)
      Listbox.insert(self, 0, item.replace("\n", "\\n"))
      self._setColors()

   #extend clipboard class function to Listbox element...
   def popStack(self):
      dock.hardPop(self)
      listpop = Listbox.get(self, 0)
      Listbox.delete(self, 0)
      self._setColors()
      return listpop

   #extend clipboard class function to Listbox element...
   def softPop(self):
      dock.softPop(self)
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
      dock.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   def indexPop(self, index):
      listLength = len(Listbox.get(self, 0, END))
      # index = Listbox.index(self, ACTIVE)
      altIndex = (listLength - 1) - index
      dock.indexPop(self, altIndex)
      if index >= 0 and index <= listLength:
         poppedItem = Listbox.get(self, index)
         Listbox.delete(self, index)
         Listbox.insert(self, 0, poppedItem)
      self._setColors()

   #extend clipboard class function to Listbox element...
   def clearStack(self):
      dock.clearDock(self)
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