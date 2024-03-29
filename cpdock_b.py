# =================================================================================================
# Copy Dock - Bravo1 
#
# clipboard stack manager with some simple text transforms.
#
# updates from Alpha:
#  - replace box-style stack display to tk 'Listbox', single-line
#  - double-click stack items to pop/add to sys clipboard
#  - add some color?
# =================================================================================================
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from clipboard_b import clipboard
from cliplist import cliplist
import transforms
import time
import json
import os
# import cx_Oracle

# This is to make touchpad scrolling smoother.  Set this to .05 or 0 if using an actual mouse.
# Need to try and find a way of unifying both models.
CLIP_LIST_SCROLL_DELAY = .1
INITIAL_FILE_SAVE_DIRECTORY = "C:\\Users\\jhessling\\Documents"

# handles writing to the boxes
class statusWriter():
   def __init__(self):
      self.textBoxHandle = None

   def setHandle(self, textBox):
      self.textBoxHandle = textBox

   def write(self, status, clearText=False, prepend=False, showEnd=True):
      entry = time.strftime('%Y-%m-%d %H:%M:%S> ', time.localtime()) + status
      self.textBoxHandle.insert(END, entry + "\n")
      if clearText:
         self.clear()
      elif showEnd:
         self.textBoxHandle.see(END)

   def clear(self, clearedMessage=""):
      self.textBoxHandle.delete(1.0, END)
      self.textBoxHandle.insert(END, clearedMessage + "\n")

class dockWindow:
   def __init__(self):
      # constant-like defs for later
      self.delimiter = '\n'
      self.wrapper = "'"
      self.separator = ','

      self.clipListLastScrollTime = time.perf_counter()

      # main tkinter element
      self.root = Tk()
      self.root.title("Copy Dock")
      self.root.rowconfigure(1, weight=1)
      self.root.columnconfigure(1, weight=1)

      # Key bindings, mainly for AutoHotkey integration.
      # Consider adding a MUCH larger variety for all functions, then publish an ICD for added user customization via the ahk script.
      self.root.bind('<Control-m>', self.addFromClipboard)
      self.root.bind('<Control-u>', self.bumpSelected)
      self.root.bind_all('<Control-MouseWheel>', self.scrollClipList)
      self.root.bind('<Control-k>', self.popClipboardStackByIndex)
      self.root.bind('<Control-space>', self.pickFromStack)
      self.root.bind('<Control-d>', self.saveToFile)

      # tkinter frames, labels, buttons, and text boxes with scrollbars and writer handlers below
      # can't decide if this is ugly or not...  consider moving some of this to functions/routines

      # top and bottom frames
      self.topFrame = Frame(self.root, borderwidth=2)
      self.topFrame.pack(fill='both', expand=1)
      self.bottomFrame = Frame(self.root)
      self.bottomFrame.pack(fill='x', expand=0)

      # the cliplist element and frames, incuding the stack
      self.clipboardListFrame = Frame(self.topFrame, borderwidth=1)
      self.clipboardListFrame.pack(side=RIGHT, fill='both', expand=1, anchor='center')
      self.clipboardListScrollBar = Scrollbar(self.clipboardListFrame, borderwidth=1)
      self.clipboardListScrollBar.pack(side=RIGHT, fill='y')
      self.mainClipboard = cliplist(self.clipboardListFrame, self.clipboardListScrollBar)
      self.mainClipboard.pack(expand=1, fill='both', anchor='n', side=TOP)
      self.clipboardListScrollBar.config(command=self.mainClipboard.yview)
      self.mainClipboard.bind('<Double-Button-1>', self.popClipboardStackByIndex)
      self.mainClipboard.bind('<Return>', self.popClipboardStackByIndex)
      self.mainClipboard.bind('<<ListboxSelect>>', self.setDisplayedCommentFromSelected)
      self.mainClipboard.bind('<Up>', self.setDisplayedCommentFromUpArrow)
      self.mainClipboard.bind('<Down>', self.setDisplayedCommentFromDownArrow)
      self.root.bind('<Control-l>', self.dumpToArchiveFileCallback)

      self.commentEntryBox = Entry(self.clipboardListFrame, relief=RAISED)
      self.commentEntryBox.delete(1, END)
      self.commentEntryBox.insert(END, "(blank)")
      self.commentEntryBox.pack(fill='x', anchor='s')
      self.commentEntryBox.bind('<Return>', self.setCommentFromEntry)
      self.commentEntryBox.bind('<FocusIn>', self.setCommentFocus)
      self.commentEntryBox.bind('<FocusOut>', self.loseCommentFocus)

      # some frames for buttons and boxes
      self.statusMessageTextFrame = Frame(self.bottomFrame)
      self.statusMessageTextFrame.pack(expand=1, fill='x', anchor='center')
      self.buttonFrame = Frame(self.topFrame, borderwidth=1)
      self.buttonFrame.pack(fill='both', side=RIGHT)
      self.entryFrame = Frame(self.buttonFrame, borderwidth=1)
      self.entryFrame.grid(column=0, row=3, sticky=(N, S, E, W), columnspan=2, rowspan=1)

      # boxes and their writers/scrollers
      self.statusMessageScrollbar = Scrollbar(self.statusMessageTextFrame, borderwidth=1)
      self.statusMessageScrollbar.pack(side=RIGHT, fill=Y)
      self.statusMessageScrollbar.bind('<Alt-MouseWheel>', self.scrollClipList)
      self.statusMessageTextBox = Text(self.statusMessageTextFrame, height=10, yscrollcommand=self.statusMessageScrollbar.set,
         background='dimgray', foreground='ghost white', insertbackground='ghost white', selectforeground='dimgray', selectbackground='ghost white')
      self.statusMessageTextBox.pack(expand=True, fill='both')
      self.statusMessageScrollbar.config(command=self.statusMessageTextBox.yview)
      self.statusMessageTextBoxWriter = statusWriter()
      self.statusMessageTextBoxWriter.setHandle(self.statusMessageTextBox)

      # entry box to choose delimiter (l-value of find-replace)
      self.delimiterLabel = Label(self.entryFrame, text="Delimiter")
      # self.delimiterLabel.grid(row=0, column=0, sticky=(N, S, E, W))
      self.delimiterLabel.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.delimiterEntryBox = Entry(self.entryFrame, width=5)
      self.delimiterEntryBox.delete(1, END)
      self.delimiterEntryBox.insert(END, "^n")
      # self.delimiterEntryBox.grid(row=0, column=1, sticky=(N, S, E, W))
      self.delimiterEntryBox.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.delimiterEntryBox.bind('<FocusIn>', self.selectDelimiterEntryAll)

      # entry box to choose separator (r-value of find-replace)
      self.separatorLabel = Label(self.entryFrame, text="Separator")
      # self.separatorLabel.grid(row=0, column=2, sticky=(N, S, E, W))
      self.separatorLabel.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.separatorEntryBox = Entry(self.entryFrame, width=5)
      self.separatorEntryBox.delete(1, END)
      self.separatorEntryBox.insert(END, ",")
      # self.separatorEntryBox.grid(row=0, column=3, sticky=(N, S, E, W))
      self.separatorEntryBox.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.separatorEntryBox.bind('<FocusIn>', self.selectSeparatorEntryAll)

      # wrapper if transform is sandwhiched
      self.wrapperLabel = Label(self.entryFrame, text="Wrapper")
      # self.wrapperLabel.grid(row=0, column=4, sticky=(N, S, E, W))
      self.wrapperLabel.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.wrapperEntryBox = Entry(self.entryFrame, width=5)
      self.wrapperEntryBox.delete(1, END)
      self.wrapperEntryBox.insert(END, "'")
      # self.wrapperEntryBox.grid(row=0, column=5, sticky=(N, S, E, W))
      self.wrapperEntryBox.pack(side=LEFT, anchor='center', fill='both', expand=1)
      self.wrapperEntryBox.bind('<FocusIn>', self.selectWrapperEntryAll)


      # Buttons below!
      self.pushbotton = ttk.Button(self.buttonFrame, text="Add From Clipboard", command=self.addFromClipboard)
      self.pushbotton.grid(column=0, row=0, sticky=(N, S, W, E), columnspan=2)
      self.pushbotton.bind('<Return>', self.addFromClipboard)

      self.hardPopButton = ttk.Button(self.buttonFrame, text="Hard Pop", command=self.popClipboardStack)
      self.hardPopButton.grid(column=1, row=1, sticky=(N, S, W, E))
      self.hardPopButton.bind('<Return>', self.popClipboardStack)

      self.softPopButton = ttk.Button(self.buttonFrame, text="Soft Pop", command=self.softPopCllipboardStack)
      self.softPopButton.grid(column=0, row=1, sticky=(N, S, W, E))
      self.softPopButton.bind('<Return>', self.softPopCllipboardStack)

      self.button1 = ttk.Button(self.buttonFrame, text="Delimiter to Separator", command=self.delimiterToSeparator, width=25)
      self.button1.grid(column=0, row=2, sticky=(N, S))
      self.button1.bind('<Return>', self.delimiterToSeparator)

      self.button2 = ttk.Button(self.buttonFrame, text="Delimiter to WrappedSep", command=self.delimiterToSeparatorWrapped, width=25)
      self.button2.grid(column=1, row=2, sticky=(N, S))
      self.button2.bind('<Return>', self.delimiterToSeparatorWrapped)

      self.clearButton = ttk.Button(self.buttonFrame, text="Clear the Dock", command=self.dxpDBTest2)
      self.clearButton.grid(column=0, row=4, sticky=(N, S, W, E), columnspan=2)
      self.clearButton.bind('<Return>', self.dxpDBTest2)

      # self.pickStackButton = ttk.Button(self.buttonFrame, text="Pick From Dock", command=self.pickFromStack)
      # self.pickStackButton.grid(column=0, row=5, sticky=(N, S, W, E), columnspan=2)
      # self.pickStackButton.bind('<Return>', self.pickFromStack)

      self.saveToFileButton = ttk.Button(self.buttonFrame, text="Save to File", command=self.saveToFile)
      self.saveToFileButton.grid(column=0, row=5, sticky=(N, S, W, E), columnspan=2)
      self.saveToFileButton.bind('<Return>', self.saveToFile)

      self.clearStatusButton = ttk.Button(self.buttonFrame, text="Clear Log", command=self.clearStatusDisplay)
      self.clearStatusButton.grid(column=0, row=6, sticky=(N, S, W, E), columnspan=2)
      self.clearStatusButton.bind('<Return>', self.clearStatusDisplay)

      self.loadFromArchiveFile()

      # vestigial - reminder of alternate convention:
      #             > set widget text elements to StringVar, will auto-update with StringVar
      self.messageText = StringVar()

   def selectDelimiterEntryAll(self, *args):
      self.delimiterEntryBox.selection_range(0, END)

   def selectSeparatorEntryAll(self, *args):
      self.separatorEntryBox.selection_range(0, END)

   def selectWrapperEntryAll(self, *args):
      self.wrapperEntryBox.selection_range(0, END)

   # clipboard list scroll handler
   def scrollClipList(self, event):
      self.mainClipboard.focus_set()
      thisTime = time.clock()
      clipListScrollDelta = thisTime - self.clipListLastScrollTime
      if clipListScrollDelta > 1 or ((clipListScrollDelta - int(clipListScrollDelta)) > CLIP_LIST_SCROLL_DELAY):
         currentSelectionList = self.mainClipboard.curselection()
         if len(currentSelectionList) == 0:
            currentSelection = 0
         else:
            currentSelection = currentSelectionList[0]
         self.mainClipboard.selection_clear(0, self.mainClipboard.size() - 1)
         if event.delta > 0:
            self.mainClipboard.selection_set(min(currentSelection + 1, self.mainClipboard.size() - 1))
            self.mainClipboard.activate(min(currentSelection + 1, self.mainClipboard.size() - 1))
         elif currentSelection >= 0:
            self.mainClipboard.selection_set(max(currentSelection - 1, 0))
            self.mainClipboard.activate(max(currentSelection - 1, 0))
         self.clipListLastScrollTime = thisTime
         self.setDisplayedCommentFromSelected(event)

   def bumpSelected(self, event):
      selected = self.mainClipboard.index(ACTIVE)
      if self.mainClipboard.focus_displayof() != self.mainClipboard:
         selected -= 1
      self.mainClipboard.focus_set()
      self.mainClipboard.selection_clear(0, self.mainClipboard.size() - 1)
      if selected >= self.mainClipboard.size() - 1:
         self.mainClipboard.selection_set(0)
         self.mainClipboard.activate(0)
      else:
         self.mainClipboard.selection_set(min(selected + 1, self.mainClipboard.size() - 1))
         self.mainClipboard.activate(min(selected + 1, self.mainClipboard.size() - 1))
      self.setDisplayedCommentFromSelected(event)


   # add to the stack
   def addClip(self, item):
      i = self.mainClipboard.isItemIn(item)
      print("i is ", i)
      if i < 0:
         self.root.clipboard_clear()
         self.mainClipboard.addItem(item)
         self.root.clipboard_append(self.mainClipboard.getCurrentItem().text)
      elif i > 0:
         print("Item ", item, "is in, at ", i)
         self.root.clipboard_clear()
         self.mainClipboard.indexPop(i)
         self.root.clipboard_append(self.mainClipboard.getCurrentItem().text)
      self.mainClipboard.dumpToArchiveFile("archive.txt")

   def setCommentFromEntry(self, *args):
      selected = self.mainClipboard.getIndex() - self.mainClipboard.index(ACTIVE)
      self.mainClipboard.setComment(self.commentEntryBox.get(), selected)
      commentMessage = "Commented: '" + self.commentEntryBox.get() + "' >> " + self.mainClipboard.get(selected)
      self.statusMessageTextBoxWriter.write(commentMessage)
      self.mainClipboard.focus_set()
      self.mainClipboard.dumpToArchiveFile("archive.txt")

   def setCommentFocus(self, *args):
      self.commentEntryBox.config(relief=SUNKEN)

   def loseCommentFocus(self, *args):
      self.commentEntryBox.config(relief=RAISED)

   def setDisplayedCommentFromSelected(self, *args):
      try:
         selected = (self.mainClipboard.getStackSize() - 1) - self.mainClipboard.curselection()[0]
         self.commentEntryBox.delete(0, END)
         self.commentEntryBox.insert(END, self.mainClipboard.getComment(selected))
      except IndexError:
         pass
      except TclError:
         pass

   def setDisplayedCommentFromUpArrow(self, event):
      self.mainClipboard.selection_clear(0, self.mainClipboard.getIndex())
      self.mainClipboard.selection_set(max(self.mainClipboard.index(ACTIVE) - 1, 0))
      self.setDisplayedCommentFromSelected(event)

   def setDisplayedCommentFromDownArrow(self, event):
      self.mainClipboard.selection_clear(0, self.mainClipboard.getIndex())
      self.mainClipboard.selection_set(min(self.mainClipboard.index(ACTIVE) + 1, self.mainClipboard.getIndex()))
      self.setDisplayedCommentFromSelected(event)

   # grab from system clipboard and add to the stack
   def addFromClipboard(self, *args):
      try:
         toAdd = str(self.root.clipboard_get())
         self.addClip(toAdd)
         self.mainClipboard.selection_clear(0, self.mainClipboard.getIndex())
         self.mainClipboard.selection_set(0)
         self.mainClipboard.activate(0)
         self.statusMessageTextBoxWriter.write("Docked: " + toAdd)
      except TclError:
         self.statusMessageTextBoxWriter.write("Error in adding from clipboard...")

   def addClipWithItem(self, item, comment="Blank"):
      self.addClip

   # pick from top of the stack, add to system clipboard
   def pickFromStack(self, *args):
      self.root.clipboard_clear()
      current = self.mainClipboard.getCurrentItem()
      if self.mainClipboard.getCurrentItem() != None:
         self.root.clipboard_append(current.text)
         self.statusMessageTextBoxWriter.write("Picked from dock: '" + current.comment + "' >> " + current.text)
         self.mainClipboard.selection_clear(0, self.mainClipboard.getIndex())
         self.mainClipboard.selection_set(0)
         self.mainClipboard.activate(0)
         self.setDisplayedCommentFromSelected()
         print("set here")
      else:
         self.statusMessageTextBoxWriter.write("Dock is empty...")

   # pop top item from clipboard stack, add next to system clipboard.
   # cycle enabled will re-insert popped item to the bottom of the stack.
   def popClipboardStack(self, *args, cycle=False):
      if cycle:
         poppedItem = self.mainClipboard.softPop()
         self.mainClipboard.dumpToArchiveFile("archive.txt")
      else:
         poppedItem = self.mainClipboard.popStack()
      if poppedItem != None and len(poppedItem) > 0:
         self.statusMessageTextBoxWriter.write('Popped: ' + poppedItem)
         self.pickFromStack(*args)
      else:
         self.statusMessageTextBoxWriter.write("Can't pop, Dock is empty...")

   # pop the clipboard stack with cycle enabled
   def softPopCllipboardStack(self, *args):
      self.popClipboardStack(self, *args, cycle=True)

   # pop clipboard stack by index
   def popClipboardStackByIndex(self, *args):
      self.mainClipboard.activePop()
      self.pickFromStack(*args)
      self.mainClipboard.dumpToArchiveFile("archive.txt")

   # clear the lower log/status display box
   def clearStatusDisplay(self, *args):
      self.statusMessageTextBoxWriter.clear("Status log is cleared...")

   # clear the system clipboard, the clipboard stack, and clipboard display box
   def clearClipboard(self, *args):
      # self.mainClipboard.clearStack()
      # self.root.clipboard_clear()
      self.statusMessageTextBoxWriter.write("Function deprecated.  For safety...")

   def dxpDBTest1(self, *args):
      # Below block is for a SPIKE to investigate extending database operations into the CopyDock.  ~JH
      self.statusMessageTextBoxWriter.write("DXP FX DB Test begin...")
      dsn = cx_Oracle.makedsn("dxpdb01u.liaison.prod", 1522, service_name="dxpuat")
      lib_dir = "C:\\Program Files\\Oracle\\instantclient_19_14\\"
      cx_Oracle.init_oracle_client(lib_dir=lib_dir)
      connection = cx_Oracle.connect(user="jhessling", password=transforms.getPassword(), dsn=dsn, encoding="UTF-8")
      cursor = connection.cursor()

      sql = """SELECT * FROM FXDXP.FX_MSG_PROPS WHERE MSG_ID LIKE 'UB35090779'"""
      cursor.execute(sql)
      for row in cursor:
         self.statusMessageTextBoxWriter.write(str(row))
      # Above block is for a SPIKE to investigate extending database operations into the CopyDock.  ~JH

   def dxpDBTest2(self, *args):
      msgID = str(self.root.clipboard_get())

      self.statusMessageTextBoxWriter.write("DXP FX DB Test begin..." + msgID)
      dsn = cx_Oracle.makedsn("dxpdb01u.liaison.prod", 1522, service_name="dxpuat")
      lib_dir = "C:\\Program Files\\Oracle\\instantclient_19_14\\"
      cx_Oracle.init_oracle_client(lib_dir=lib_dir)
      connection = cx_Oracle.connect(user="jhessling", password=transforms.getPassword(), dsn=dsn, encoding="UTF-8")
      cursor = connection.cursor()

      sql = """SELECT * FROM FXDXP.FX_MSG_PROPS WHERE MSG_ID LIKE :query_msgid"""
      cursor.execute(sql, query_msgid=msgID)
      for row in cursor:
         self.statusMessageTextBoxWriter.write(str(row))

   # no longer used, outdated
   def newlineToComma(self, *args):
      try:
         toTransform = str(self.root.clipboard_get())
      except TclError:
         self.statusMessageTextBoxWriter.write("Error in executing newlineToComma transform, stack probably empty...")

      self.addClip(transforms.sep(toTransform))
      self.statusMessageTextBoxWriter.write("Newline to comma transform applied...")

   # grab delimiter and separator from boxes, find/replace
   def delimiterToSeparator(self, *args):
      try:
         toTransform = str(self.root.clipboard_get())
      except TclError:
         self.statusMessageTextBoxWriter.write("Error in executing transform, Dock probably empty...")

      separator = self.getSeparator()
      delimiter = self.getDelimiter()
      self.addClip(transforms.sep(toTransform, delimiter, separator))
      self.statusMessageTextBoxWriter.write("Delimiter to Separator transform applied...")

   # do delimiterToSeparator, wrap it with wrapper from box
   def delimiterToSeparatorWrapped(self, *args):
      try:
         toTransform = str(self.root.clipboard_get())
      except TclError:
         self.statusMessageTextBoxWriter.write("Error in executing transform, Dock probably empty...")

      separator = self.getSeparator()
      delimiter = self.getDelimiter()
      wrapper = self.getWrapper()
      self.addClip(transforms.wrapSep(toTransform, delimiter, separator, wrapper))
      self.statusMessageTextBoxWriter.write("Delimiter to Separator transform applied...")

   # grab delimiter from the entry box
   def getDelimiter(self):
      delimiter = self.delimiterEntryBox.get()
      delimiter = transforms.fixPattern(delimiter)
      if delimiter == None:
         delimiter = self.delimiter
      return delimiter

   # grab separator from the entry box
   def getSeparator(self):
      separator = self.separatorEntryBox.get()
      separator = transforms.fixPattern(separator)
      if separator == None or separator == "":
         separator = self.separator
      return separator

   # grab wrapper from the entry box
   def getWrapper(self):
      wrapper = self.wrapperEntryBox.get()
      wrapper = transforms.fixPattern(wrapper)
      if wrapper == None:
         wrapper = self.wrapper
      return wrapper

   # def syncComments(self):
   #    self.commentEntryBox.delete(0, END)
   #    self.commentEntryBox.insert(END, self.mainClipboard.getCurrentItem().comment)

   # the go-button
   def drawWindow(self):
      self.root.mainloop()

   def dumpToArchiveFileCallback(self, event):
      self.mainClipboard.dumpToArchiveFile("archive.txt")

   def loadFromArchiveFile(self, filename="archive.txt"):
      try:
         with open(filename) as archiveFileHandle:
            archiveContents = json.load(archiveFileHandle)

         for a in archiveContents:
            self.mainClipboard.addItemWithComment(a['text'], a['comment'])
            print(a['text'], a['comment'])

         self.statusMessageTextBoxWriter.write("Successfully loaded saved Dock from archives...")
      except FileNotFoundError:
         pass
      except json.decoder.JSONDecodeError:
         pass

   def saveToFile(self, *args):
      try:
         toAdd = str(self.root.clipboard_get())
         filename = filedialog.asksaveasfilename(initialdir=INITIAL_FILE_SAVE_DIRECTORY, title="Please select filename and location...")
         # print(filename)
         with open(filename, "w+") as copyFileHandle:
            copyFileHandle.write(toAdd)
         self.statusMessageTextBoxWriter.write("Successfully wrote clipboard contents to '" + filename + "'!")
         os.startfile(filename)

      except TclError:
         self.statusMessageTextBoxWriter.write("Error in adding from clipboard...")

