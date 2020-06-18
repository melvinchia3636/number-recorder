#!/usr/bin/python
# -*- coding: utf-8 -*-

# import needed library
from tkinter import *
from tkinter.font import Font
import tkinter.messagebox as ms
import csv 
import os

# initialize window
root = Tk() 
root.config(bg='white') 
root.title('Quick Variables Recorder')
root.iconbitmap('icon.ico') 
root.wm_attributes('-topmost', 1) 
root.resizable(False, False) 

# globalize all the font settings so all function can use them
global framefont 
global inputfont 
global titlefont
global buttonfont

# the font settings
framefont = Font(size=20, family='Bahnschrift Light')
inputfont = Font(size=20, family='Courier') 
titlefont = Font(size=30, family='Bahnschrift SemiBold')
buttonfont = Font(size=15, family='Bahnschrift Light') 

# transition function between openfile page to edit page
def edithelp():
    namelist.grid_forget() 
    filename_input.grid_forget() 
    filenameinputframe.grid_forget() 
    buttonopendb.grid_forget()
    filenameshowframe.grid_forget()

    global v
    (v, v2) = ([], [])
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        [v2.append(row) for row in csvReader]
        [v.append(i) for i in v2[0]]
    edit()


# openfile page
def editdb():
    global namelist
    global filename_input
    global filenameinputframe
    global buttonopendb
    global filenameshowframe
    global filesname

    buttoncreate.grid_forget()
    buttonedit.grid_forget()
    buttonsettings.grid_forget()

    root.geometry('500x400')

  # setup the filename
    def openfilelol():
        global filename
        filename = 'database/' + filename_input.get()
        edithelp()

  # detect if the input is being clicked
    def fileon_click(event):
        filename_input.configure(state=NORMAL)
        filename_input.delete(0, END)
        filename_input.unbind('<Button-1>', fileon_click_id)

    namescrollbar = Scrollbar(root)
    
    filenameshowframe = Frame(
        root,
        background='BLACK',
        borderwidth=1,
        relief=FLAT
        )
    
    namelist = Listbox(
        filenameshowframe,
        yscrollcommand=namescrollbar.set,
        width=20,
        relief=FLAT,
        height=4,
        font=framefont,
        justify=CENTER,
        )
    
    namescrollbar.config(command=namelist.yview)

    extension = '.csv'
    path = 'database/'
    filesname = []

    if os.path.exists(str(path)) == True:
        for (r, d, f) in os.walk(path):
            for file in f:
                if extension in file:
                    filesname.append(os.path.join(file))

    fileamount = len(filesname)

    [namelist.insert(END, filesname[a]) for a in range(fileamount)]

    filenameinputframe = Frame(
        root,
        background='BLACK',
        borderwidth=1
        )
    
    filename_input = Entry(
        filenameinputframe,
        font=inputfont,
        borderwidth=0,
        relief=FLAT,
        justify=CENTER,
        width=20,
        bg='white',
        )

  # detect if mouse touch the button
    def buttonopendb_on_enter(e):
        buttonopendb['background'] = '#CFCFCF'
        buttonopendb['fg'] = 'white'
    def buttonopendb_on_leave(e):
        buttonopendb['background'] = 'white'
        buttonopendb['fg'] = 'black'

    buttonopendb = Button(
        root,
        text='open',
        width=20,
        font=buttonfont,
        activebackground='#CFCFCF',
        activeforeground='white',
        highlightbackground='black',
        highlightthickness=10,
        relief=SOLID,
        bg='white',
        command=openfilelol,
        )

    filenameshowframe.grid(row=1, column=0, pady=10, padx=58)
    namelist.grid(row=1, column=0)
    filenameinputframe.grid(row=2, column=0, pady=15)
    filename_input.grid(row=2, column=0, ipady=5)
    buttonopendb.grid(row=3, column=0)
    
    filename_input.insert(0, 'database name here')
    filename_input.configure(state=DISABLED)
    fileon_click_id = filename_input.bind('<Button-1>', fileon_click)
    buttonopendb.bind('<Enter>', buttonopendb_on_enter)
    buttonopendb.bind('<Leave>', buttonopendb_on_leave)


# transition between createfile page to edit page
def toedit():
    global v
    
    nameinputframe.grid_forget()
    name_input.grid_forget()
    buttoncreatedb.grid_forget()
    
    v = []
    
    edit()


# edit page
def edit():
    global inputcol
    global mylist
    global varshowframe
    global inputcolframe

    root.geometry('500x330')

    scrollbar = Scrollbar(root)
    
    varshowframe = Frame(
        root,
        background='BLACK',
        borderwidth=1,
        relief=FLAT
        )
    
    mylist = Listbox(
        varshowframe,
        yscrollcommand=scrollbar.set,
        width=20,
        relief=FLAT,
        height=4,
        font=framefont,
        justify=CENTER,
        )

  # refresh the page whenever enter key pressed
    def refresh():
        mylist.delete(0, END)
        [mylist.insert(END, v[i]) for i in range(len(v))]
        mylist.see(len(v))

  # get the user input
    def get(event):
        global inputcol
        
        if event.widget.get() == '/':
            v.pop()
            inputcol.delete(0, END)
            
            refresh()
            
        elif event.widget.get() == '+':
            with open(filename, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(v)
                
            varshowframe.grid_forget()
            mylist.grid_forget()
            inputcolframe.grid_forget()
            inputcol.grid_forget()
            
            create()
            
        else:
            v.append(event.widget.get())
            inputcol.delete(0, END)
            
            refresh()

    inputcolframe = Frame(root, background='#C7C7C7', borderwidth=1)
    inputcol = Entry(
        inputcolframe,
        font=inputfont,
        borderwidth=0,
        relief=FLAT,
        justify=CENTER,
        width=20,
        bg='white',
        )
    
    inputcol.bind('<Return>', get)

    scrollbar.config(command=mylist.yview)

    [mylist.insert(END, v[i]) for i in range(len(v))]

    refresh()

    varshowframe.grid(row=1, column=0, pady=10, padx=58)
    mylist.grid(row=1, column=0)
    inputcolframe.grid(row=2, column=0, pady=15)
    inputcol.grid(row=2, column=0, ipady=5)


# create file page
def create():
    global root
    global name_input
    global nameinputframe
    global buttoncreatedb

  # check if the file exist
    def createfile():
        global filename
        global name_input
        
        filename = 'database/' + str(name_input.get()) + '.csv'

        if os.path.isfile(filename):
            ms.showwarning('Stupid', 'File already exist')
            
        else:
            toedit()

  # check if the input box is being clicked
    def on_click(event):
        name_input.configure(state=NORMAL)
        name_input.delete(0, END)
        name_input.unbind('<Button-1>', on_click_id)

  # checked if button is being hover by mouse
    def buttoncreatedb_on_enter(e):
        buttoncreatedb['background'] = '#CFCFCF'
        buttoncreatedb['fg'] = 'white'
    def buttoncreatedb_on_leave(e):
        buttoncreatedb['background'] = 'white'
        buttoncreatedb['fg'] = 'black'

    buttoncreate.grid_forget()
    buttonedit.grid_forget()
    buttonsettings.grid_forget()

    nameinputframe = Frame(root, background='#C7C7C7', borderwidth=1)
    
    name_input = Entry(
        nameinputframe,
        font=inputfont,
        borderwidth=0,
        relief=FLAT,
        justify=CENTER,
        width=20,
        bg='white',
        )

    buttoncreatedb = Button(
        root,
        text='create',
        width=20,
        font=buttonfont,
        activebackground='#CFCFCF',
        activeforeground='white',
        highlightbackground='black',
        highlightthickness=10,
        relief=SOLID,
        bg='white',
        command=createfile,
        )

    nameinputframe.grid(row=1, column=0, pady=15)
    name_input.grid(row=1, column=0, ipady=5)
    buttoncreatedb.grid(row=2, column=0)
    
    name_input.insert(0, 'database name here')
    name_input.configure(state=DISABLED)
    on_click_id = name_input.bind('<Button-1>', on_click)
    buttoncreatedb.bind('<Enter>', buttoncreatedb_on_enter)
    buttoncreatedb.bind('<Leave>', buttoncreatedb_on_leave)


# mainmenu
def mainmenu():
    global root
    global buttoncreate
    global buttonedit
    global buttonsettings
    
    root.geometry('500x330')

  # checked if the button is being hovered by the mouse
    def buttoncreate_on_enter(e):
        buttoncreate['background'] = '#CFCFCF'
        buttoncreate['fg'] = 'white'
    def buttoncreate_on_leave(e):
        buttoncreate['background'] = 'white'
        buttoncreate['fg'] = 'black'

    def buttonedit_on_enter(e):
        buttonedit['background'] = '#CFCFCF'
        buttonedit['fg'] = 'white'
    def buttonedit_on_leave(e):
        buttonedit['background'] = 'white'
        buttonedit['fg'] = 'black'

    def buttonsettings_on_enter(e):
        buttonsettings['background'] = '#CFCFCF'
        buttonsettings['fg'] = 'white'
    def buttonsettings_on_leave(e):
        buttonsettings['background'] = 'white'
        buttonsettings['fg'] = 'black'

    title = Label(
        root,
        text='QUICK VAR RECORDER',
        font=titlefont,
        bg='white'
        )

    buttoncreate = Button(
        root,
        text='create new database',
        width=20,
        font=buttonfont,
        activebackground='#CFCFCF',
        activeforeground='white',
        highlightbackground='black',
        highlightthickness=10,
        relief=SOLID,
        bg='white',
        command=create,
        )

    buttonedit = Button(
        root,
        text='edit database',
        width=20,
        font=buttonfont,
        activebackground='#CFCFCF',
        activeforeground='white',
        highlightbackground='black',
        highlightthickness=10,
        relief=SOLID,
        bg='white',
        command=editdb,
        )

    buttonsettings = Button(
        root,
        text='settings',
        width=20,
        font=buttonfont,
        activebackground='#CFCFCF',
        activeforeground='white',
        highlightbackground='black',
        highlightthickness=10,
        relief=SOLID,
        bg='white',
        )

    title.grid(row=0, column=0, pady=15, padx=35)
    buttoncreate.grid(row=1, column=0)
    buttonedit.grid(row=2, column=0, pady=15)
    buttonsettings.grid(row=3, column=0)

    buttoncreate.bind('<Enter>', buttoncreate_on_enter)
    buttoncreate.bind('<Leave>', buttoncreate_on_leave)
    buttonedit.bind('<Enter>', buttonedit_on_enter)
    buttonedit.bind('<Leave>', buttonedit_on_leave)
    buttonsettings.bind('<Enter>', buttonsettings_on_enter)
    buttonsettings.bind('<Leave>', buttonsettings_on_leave)

mainmenu()

root.mainloop()
