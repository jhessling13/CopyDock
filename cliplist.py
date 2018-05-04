# =================================================================================================
#
# Clip List
#
# Love-child of text-based clipboard class and tkinter Listbox class
# 
# Some ugly code below, could use some refactoring.
# =================================================================================================
from tkinter import *

from clipboard import clipboard


class cliplist(clipboard, Listbox):
    def __init__(self, topFrame, scrollbar):
        clipboard.__init__(self)
        self.cliplist = Scrollbar(topFrame)
        Listbox.__init__(self, topFrame, yscrollcommand=scrollbar.set, selectmode=SINGLE)

    # Add a clip to the dock
    def addItem(self, item, comment=""):
        clipboard.addItem(self, item, comment)
        Listbox.insert(self, 0, item.replace("\n", "\\n"))
        self._setColors()

    # Remove item from top of stack/dock
    def popStack(self):
        clipboard.popStack(self)
        listpop = Listbox.get(self, 0)
        Listbox.delete(self, 0)
        self._setColors()
        return listpop

    # Perform a pop, but replace item at the back of the stack/dock
    def softPop(self):
        clipboard.softPop(self)
        listpop = Listbox.get(self, 0)
        Listbox.delete(self, 0)
        if len(listpop) > 0:
            Listbox.insert(self, END, listpop)
            self._setColors()
            return listpop
        return None

    # Perform the pop by a given index
    def indexPop(self, index):
        listLength = len(Listbox.get(self, 0, END))
        altIndex = (listLength - 1) - index
        clipboard.indexPop(self, altIndex)
        if 0 <= index <= listLength:
            poppedItem = Listbox.get(self, index)
            Listbox.delete(self, index)
            Listbox.insert(self, 0, poppedItem)
        self._setColors()

    # Perform indexPop by the current active item in the UI
    def activePop(self):
        listLength = len(Listbox.get(self, 0, END))
        index = Listbox.index(self, ACTIVE)
        altIndex = (listLength - 1) - index
        clipboard.indexPop(self, altIndex)
        if 0 <= index <= listLength:
            poppedItem = Listbox.get(self, index)
            Listbox.delete(self, index)
            Listbox.insert(self, 0, poppedItem)
        self._setColors()

    # dump everything
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
                Listbox.itemconfig(self, a, bg='gainsboro', selectbackground='SlateGray1', selectforeground='black')
