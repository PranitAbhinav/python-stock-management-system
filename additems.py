import sqlite3
import tkMessageBox
import mainfile

productidnos=sqlite3.connect('hi.db')
cur2=productidnos.cursor()
cur2.execute('''CREATE TABLE if not exists number
             (pid integer id,num integer)''')

productidnos.commit()
cur2.execute("SELECT * FROM number ")
temp=cur2.fetchall()
#######___________Product DATABASE SQLITE________________####################
#############################################################################

def scanit():
    import barscanner
    global root,scan,lab
    scan=barscanner.barscan()
    lab.destroy()
    Label(root, text="Scan recieved",fg='green').grid(row=1, column=1)
from Tkinter import *
def addnew():
    global list,cur1
    list = sqlite3.connect('list_of_products.sqlite')
    cur1 = list.cursor()
    cur1.execute('''CREATE TABLE if not exists itemlist
                    (proid integer id,    
                     scan text,
                     name text,
                     category text,
                     manufacturer text,
                     addqnty text,
                     cost text)
                    ''')

    global lab,root,scan
    scan=''
    root=Tk()
    root.geometry('400x500+0+0')
    Label(root,text="welcome you can scan new products here").grid(row=0,column=0)
    Button(root,text="SCAN",command=scanit,width=30).grid(row=1,column=0)
    lab=Label(root,text="No Scan available",fg='red')
    lab.grid(row=1, column=1)
    global productid,nameV,categoryV,manufacturerV,addqntyV,costV
    nameV = StringVar(root)
    categoryV = StringVar(root)
    manufacturerV = StringVar(root)
    addqntyV = StringVar(root)
    costV=StringVar(root)
    Label(root, text='Name of Product:').grid(row=3, column=0)
    name = Entry(root, textvariable=nameV).grid(row=3, column=1)
    Label(root, text='category:').grid(row=4, column=0)
    category = Entry(root, textvariable=categoryV).grid(row=4, column=1)
    Label(root, text='Manufaxtured by').grid(row=5, column=0)
    manufacturer = Entry(root, textvariable=manufacturerV).grid(row=5, column=1)
    Label(root, text='cost').grid(row=6, column=0)
    cost = Entry(root, textvariable=costV).grid(row=6, column=1)
    Label(root, text='Quantity:').grid(row=7, column=0)
    addqnty = Entry(root, textvariable=addqntyV).grid(row=7, column=1)
    sub = Button(root, text="submit", command=submit, width=22).grid(row=8, column=1)

    Button(root, text='Main Menu',width=22, activebackground='orange', bg='light goldenrod',
           command=mainmenu).grid(row=9, column=1)
    root.mainloop()
def mainmenu():
    global root
    root.destroy()
    mainfile.show()

def submit():
        global root,scan,nameV,categoryV,manufacturerV,addqntyV,costV,productid,cur1,list
        print [scan, nameV.get(), categoryV.get(), manufacturerV.get(), addqntyV.get(), costV.get()]
        if  scan =='' or nameV.get() =='' or categoryV.get()=='' or manufacturerV.get()=='' or addqntyV.get()=='' or costV.get()=='':
            tkMessageBox.showinfo('message', message="Looks like You have left some box empty")
        else:

            print "create product id and enter information"
            productid = temp[0][1]+1
            cur2.execute('''UPDATE number SET num = ? WHERE pid = ? ''',
                           (productid, 0))
            productidnos.commit()
            cur2.execute("SELECT * FROM number ")

            temp2=cur2.fetchall()

            productidnos.commit()

            productidnos.close()

            cur1.execute('''INSERT INTO itemlist (proid,scan,name,category,manufacturer,addqnty,cost) VALUES(?,?,?,?,?,?,?)''',
                                                  (productid,scan,nameV.get(),categoryV.get(),manufacturerV.get(),addqntyV.get(),costV.get()))
            list.commit()
            list.close()
            root.destroy()
            tkMessageBox.showinfo('message', message="Product succesfully updated")
            mainfile.show()
