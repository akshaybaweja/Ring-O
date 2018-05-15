from tkinter import *
import os, subprocess, re

root = Tk()

class mainWindow:

    def __init__(self, master):
        self.root = master
        self.mode = StringVar()

        self.root.title("Ring - O")
        self.root.geometry("800x600")
        self.mode.set("Select Mode")
        
        self.titlelabel = Label(self.root, textvariable=self.mode)
        self.mainFrame = LabelFrame(self.root, labelwidget=self.titlelabel, padx=10, pady=10)
        
        self.statusbar = statusBar(root)
        self.menubar = menuBar(root, self)

        self.displayLabel = Label(self.mainFrame, text="", font=("Helvetica", 80))
        self.displayLabel.pack(fill=BOTH)

        self.mainFrame.pack(fill=BOTH, expand=TRUE)
        self.update_clock()

    def updateMode(self, mode):
        self.mode.set(mode)
        self.statusbar.updateStatusBar("Running " + self.mode.get() +" Mode")

    def update_clock(self):
        if self.mode.get() != "Select Mode":
            input_file = open(self.mode.get() + "/output.txt")
            self.displayLabel.configure(text=input_file.read())
            input_file.close()

        self.mainFrame.after(100, self.update_clock)
    
    def quit(self):
        self.root.destroy()

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
        self.toolMenu.add_command(label="Predict", command=self.predict)
        self.toolMenu.add_command(label="End Predict", command=self.endPredict)
        self.menu.add_cascade(label="Tools", menu=self.toolMenu)

        self.helpMenu = Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)

        self.root.config(menu=self.menu)

    def modeCallback(self):
        if self.parentClass != None:
            self.parentClass.updateMode(self.mode.get())
    
    def trainLetter(self):
        top = Toplevel()
        top.title("Train Letter")

        letter = StringVar()
        labelLetterEntry = Label(top, text="Enter Letter")
        labelLetterEntry.grid(row=0, column=0)
        letterEntry = Entry(top, textvariable=letter)
        letterEntry.grid(row=0, column=1)

        batch = StringVar()
        labelBatchEntry = Label(top, text="Enter Batch")
        labelBatchEntry.grid(row=1, column=0)
        batchEntry = Entry(top, textvariable=batch)
        batchEntry.grid(row=1, column=1)

        trainButton = Button(top, text="Start Sampling", command=lambda: self.trainTask("Keyboard", letter.get(), batch.get()))
        trainButton.grid(row=2, columnspan=2)

    def trainGesture(self):
        top = Toplevel()
        top.title("Train Gesture")

        letter = StringVar()
        labelLetterEntry = Label(top, text="Enter Gesture Letter")
        labelLetterEntry.grid(row=0, column=0)
        letterEntry = Entry(top, textvariable=letter)
        letterEntry.grid(row=0, column=1)

        batch = StringVar()
        labelBatchEntry = Label(top, text="Enter Batch")
        labelBatchEntry.grid(row=1, column=0)
        batchEntry = Entry(top, textvariable=batch)
        batchEntry.grid(row=1, column=1)

        trainButton = Button(top, text="Start Sampling", command=lambda: self.trainTask("Gesture", letter.get(), batch.get()))
        trainButton.grid(row=2, columnspan=2)

    def trainTask(self, type, letter, batch):
        os.system("ttab -t 'training' 'cd "+type+" && python start.py target="+letter+":"+batch+"'")

    def learn(self):
        top = Toplevel()
        top.title("Learn | Output")
        
        output = subprocess.check_output("cd "+self.mode.get()+" && python learn.py", shell=True)
        
        acc = "New Model Accuracy: " + str(round(float(re.search('SCORE: (\d*.\d*)', output).group(1))*100, 2))+" %"
        accuracy = Label(top, font=('Monaco',20, "bold"), text=acc, pady=10, bg="black", fg="white")
        accuracy.pack(fill=X)

        msg = Text(top, font=('Monaco',14), height=40)
        msg.insert(INSERT, output)
        msg.pack(fill=BOTH)

    def predict(self):
        
        if self.mode.get() == "Keyboard":
            self.t = subprocess.call("ttab -t 'predict' 'cd Keyboard && python start.py write'", shell=True)
            
        elif self.mode.get() == "Gesture":
            self.t = subprocess.call("ttab -t 'predict' 'cd Gesture && python start.py gesture'", shell=True)
    
    def endPredict(self):
        scriptEndProgram = "osascript -e 'tell application "+'"Terminal"' +" to close windows where name contains "+'"predict"'+"'"
        os.system(scriptEndProgram)

    def about(self):
        top = Toplevel()
        top.title("About Ring-O")

        about_message = "M A J O R    S U B M I S S I O N\n\nRing-O is a three dimensional, gesture-based input tool that lets you type in the air and display the content on a screen. The whole device is designed in the form of a ring which connects to the PC via Bluetooth. The ring is packed with micro- controller, IMUs like accelerator and gyroscope, battery along with protection circuit and a bluetooth module.\n\nSubmitted by -\nAkshay Baweja (00713202814)\nDivya Koneti (00913201814)"
        msg = Message(top, text=about_message, font=('Helvetica',16), aspect=200)
        msg.pack()
    
    def quit(self):
        if self.parentClass != None:
            self.parentClass.quit()

class statusBar:

    def __init__(self, master):
        self.root = master

        self.statusText = StringVar()
        self.status = Label(root, textvariable = self.statusText, relief = RAISED, bd=1, anchor=W)
        self.statusText.set("Running")
        self.status.pack(side=BOTTOM, fill=X)

    def updateStatusBar(self, text):
        self.statusText.set(text)

os.system("find . -name '.DS_Store' -type f -delete")

mainWindow(root)

root.mainloop()