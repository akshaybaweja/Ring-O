from tkinter import *

root = Tk()

class mainWindow:

    def __init__(self, master):
        self.root = master

        self.root.title("Ring - O")
        self.mainFrame = Frame(self.root, width=800, height=600)

        self.statusbar = statusBar(root)
        self.menubar = menuBar(root, self)

        self.mainFrame.pack()

    def updateMode(self, mode):
        self.statusbar.updateStatusBar("Running " + mode +" Mode")

class menuBar:
    def __init__(self, master, parent = None):
        self.root = master
        self.parentClass = parent
        self.mode = StringVar()
        
        self.menu = Menu(root)
        self.modeMenu = Menu(self.menu, tearoff=0)
        self.modeMenu.add_radiobutton(label="Keyboard Mode", variable=self.mode, value="Keyboard", underline=0, command=self.modeCallback)
        self.modeMenu.add_radiobutton(label="Gesture Mode", variable=self.mode, value="Gesture", underline=0, command=self.modeCallback)
        self.modeMenu.add_separator()
        self.modeMenu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="Mode", menu=self.modeMenu)

        self.toolMenu = Menu(self.menu, tearoff=0)
        self.toolMenu.add_command(label="Train New Letter", command=self.trainLetter)
        self.toolMenu.add_command(label="Train New Gesture", command=self.trainGesture)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Learn", command=self.learn)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Predict Letters", command=self.predictLetter)
        self.toolMenu.add_command(label="Predict Gesture", command=self.predictGesture)
        self.menu.add_cascade(label="Tools", menu=self.toolMenu)

        self.helpMenu = Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)

        self.root.config(menu=self.menu)

    def modeCallback(self):
        if self.parentClass != None:
            self.parentClass.updateMode(self.mode.get())
    
    def trainLetter(self):
        print "train Letter"

    def trainGesture(self):
        print "train Gesture"

    def learn(self):
        print "learn"

    def predictGesture(self):
        print "predict Gesture"
    
    def predictLetter(self):
        print "predict Letter"

    def about(self):
        print "about"
    
    def quit(self):
        print "quit"

class statusBar:

    def __init__(self, master):
        self.root = master
        self.statusText = StringVar()
        self.status = Label(root, textvariable = self.statusText, relief = RAISED, bd=1, anchor=W)
        
        self.statusText.set("Running")

        self.status.pack(side=BOTTOM, fill=X)

    def updateStatusBar(self, text):
        self.statusText.set(text)

mainWindow(root)

root.mainloop()