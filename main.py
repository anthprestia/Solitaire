from tkinter import *
from tkinter import ttk
import random
import os


def changeColor(widget):
    colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
    i = random.randint(0, len(colors) - 1)
    color = colors[i]
    print(color)

    widget.configure(text=color)

def addToListbox(lbox, entry):
    if entry.get() != "":
        lbox.insert(END, entry.get())

def removeFromListbox(lbox):
    idx = lbox.curselection()
    if len(idx) == 1:
        lbox.delete(idx[0])
        # if the element gets deleted from the list that index in the list gets deselected
        # when deleted, check to see if lbox size > index
        if lbox.size() > idx[0]:
            lbox.select_set(idx[0])
            #lbox.activate(idx[0])
        else:
            lbox.select_set(idx[0]-1)
            #lbox.activate(idx[0]-1)


def openWindow():

    # The 'root' of the whole UI
    root = Tk()
    # Trying to assign a custom size with min/max value for stretching the screen
    root.geometry("500x500")
    root.minsize(200, 200)
    root.maxsize(800, 800)

    mainframe = ttk.Frame(root, padding=10)
    mainframe.pack()
    ttk.Label(mainframe, text="Hello World!").grid(column=0, row=0)
    ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=1, row=0)

    flist = Listbox(mainframe, width=30, height=10, bg='red',)
    flist.grid(column=0, row=1)
    flist.insert(END, 'snowman.txt')
    flist.insert(END, 'apple.gif')

    changeButton = ttk.Button(mainframe, text='Change Color')
    #changeButton.config(command=lambda: changeColor(changeButton))
    changeButton.configure(command=lambda: changeColor(changeButton))
    changeButton.grid(column=1, row=1)

    entry = StringVar()
    entryBox = Entry(mainframe, textvariable=entry)
    entryBox.grid(column=0, row=2)

    addButton = Button(mainframe, text='Add', command=lambda: addToListbox(flist, entry))
    addButton.grid(column=1, row=2)

    removeButton = Button(mainframe, text='Remove', command=lambda: removeFromListbox(flist))
    removeButton.grid(column=2, row=2)

    # Last actions
    root.mainloop()
    return root

def configEnv():
    # make sure a file directory is around to store files.
    cwd = os.getcwd()
    fileFolder = cwd + "/files"

    if not os.path.exists(fileFolder):
        os.makedirs(fileFolder)

def main():
    #cwd is project directory
    configEnv()
    root = openWindow()

if __name__ == '__main__':
    main()