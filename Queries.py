import pandas as pd
import sqlite3
#from PIL import ImageTk, Image

#from PIL import Image
import PIL.Image

import tkMessageBox
from Tkinter import *
import difflib
def patrn(t1,t2):
    seq=difflib.SequenceMatcher(isjunk=None,a=t1,b=t2)
    return seq.ratio()


def Query():
    global mroot
    mroot=Tk()
    mroot.geometry('500x400')
    global var
    #import PIL.Image
    #fp = open("queries.png",'rb')
    #img = PIL.Image.open(fp)
    #lab=Label(mroot,img)
    #lab.place(x=250,y=200,anchor=N)


    var=StringVar(mroot)
    var.set("SELECT TYPE OF QUERY HERE")
    Label(mroot,text='Search',font=('times',42, 'bold'),fg='black').place(x=180,y=1,anchor=N)
    Label(mroot,text='your',font=('times',28, 'italic'),fg='black').place(x=335,y=22,anchor=N)

    Label(mroot,text='QUERIES',font=('times',68, 'bold'),fg='coral').place(x=250,y=70,anchor=N)
    Label(mroot,text='SELECT:',font=('times',11, 'bold'),fg='black').place(x=150,y=203,anchor=N)

    cashmode = OptionMenu(mroot, var, "Customer Query", "Product Query").place(x=290,y=200,anchor=N)
    Button(mroot,text="PROCEED..",font=('times',17, 'bold'),height=1,command=begin).place(x=250,y=250,anchor=N)
    mroot.mainloop()
def begin():
    global var
    if var.get()=="SELECT TYPE OF QUERY HERE":
        tkMessageBox.showinfo(message="NO OPTION SELECTED ")
    elif var.get()=="Customer Query":
        Querypersons()
    elif var.get()=="Product Query":
        Queryprduct()



###################################################################################$####$#$#$#$#$#$#$#$#$#$#$###$#
def Querypersons():
    global root,mroot,namecq,cashcq,phnocq,datecq
    mroot.destroy()
    root=Tk()
    namecq=StringVar(root)
    cashcq=StringVar(root)
    phnocq=StringVar(root)
    datecq=StringVar(root)
    Label(root,text="ENTER SOME DATA TO PROCEED WITH QUERY:").grid(row=3,column=0,columnspan=2)
    Label(root, text="Customer Name :").grid(row=4, column=0)
    Label(root, text="Cashmode:").grid(row=5, column=0)
    Label(root, text="Phone number:").grid(row=6, column=0)
    cashcq.set("Select one")
    Entry(root, textvariable=namecq, width=50).grid(row=4, column=1)
    #Entry(root, textvariable=cashcq, width=50).grid(row=5, column=1)
    cashmode = OptionMenu(root, cashcq, "Debit Card", "Credit Card", "CASH","Membership Points").grid(row=5, column=1)

    Entry(root, textvariable=phnocq, width=50).grid(row=6, column=1)
    Button(root,text="SEARCH",command=srchcq,font=('times',17, 'bold')).grid(row=8,columnspan=2)

global searchcq

def srchcq():

    global root, namecq, cashcq, phnocq,searchcq
    searchcq=[]
    if namecq.get() == "" and cashcq.get() == "Select one" and phnocq.get()=="":
        tkMessageBox.showinfo(message="All Fields are empty")
    else:
        a = sqlite3.connect("bills.db")
        if namecq.get() == "" and phnocq.get() == "":
            df = pd.read_sql("select * from billdetail where cashmode=(?)", a,params=(cashcq.get(),))
            for i in df.values.tolist():
                if i not in searchcq: searchcq.append(i)
        if namecq.get()!="":
            searchthecq(namecq.get(),'name')
        if phnocq.get()!="":
            searchthecq(phnocq.get(),'phoneno')
        if searchcq==[]:
            tkMessageBox.showinfo(message="No Close records found")
        else:
            root.destroy()
            display()

def display():
    dis=[]
    global disp
    disp=Tk()
    line=3
    Label(disp,text="Here are the results of your Query:",font=('times',15, 'bold'))
    Label(disp, text="ref", relief='ridge',width=15).grid(row=2, column=0)
    Label(disp, text="Name", relief='ridge',width=15).grid(row=2, column=1)
    Label(disp, text="cashmode", relief='ridge',width=15).grid(row=2, column=2)
    Label(disp, text="phone no.", relief='ridge',width=15).grid(row=2, column=3)
    Label(disp, text="date", relief='ridge',width=15).grid(row=2, column=4)
    Label(disp, text="time", relief='ridge',width=15).grid(row=2, column=5)

    for i in searchcq:
        dis.append(i[0])
        Label(disp, text=i[0], width=15).grid(row=line, column=0)
        Label(disp, text=i[1], width=15).grid(row=line, column=1)
        Label(disp, text=i[2], width=15).grid(row=line, column=2)
        Label(disp, text=i[3], width=15).grid(row=line, column=3)
        liss=i[4][1:-1].split(", ")
        Label(disp, text=liss[2]+"/"+liss[1]+"/"+liss[0], width=15).grid(row=line, column=4)
        Label(disp, text=liss[3]+":"+liss[4], width=15).grid(row=line, column=5)
        line+=1
    Label(disp,text="").grid(row=line)
    Label(disp,text="").grid(row=line+1)
    Button(disp,text="Main Menu",command=MAIN).grid(row=line+3,columnspan=2)
    disp.mainloop()

def productinf(x):
        print x



def MAIN():
    global disp
    disp.destroy()
    import mainfile
    mainfile.show()
def searchthecq(value, x):
    global searchcq
    a = sqlite3.connect("bills.db")
    df = pd.read_sql("select * from billdetail", a)
    if value in df[x].values.tolist():
        df1 = df.loc[df[x].isin([value])]
        for i in df1.values.tolist():
            if i not in searchcq:
                searchcq.append(i)
    else:
        for i in df[x].values.tolist():
            percen=0.45

            if patrn(value, str(i)) > percen:
                df2 = df.loc[df[x].isin([i])]
                for i2 in df2.values.tolist():
                    if i2 not in searchcq:
                        searchcq.append(i2)







########################################################################################################$#$#$##$###
def Queryprduct():
    global rootpro,mroot
    mroot.destroy()
    rootpro=Tk()
    rootpro.geometry("410x190")


    global namepq,idpq,scnpq,manfacpq,cstpq
    global searchlist,searchlist2
    searchlist=[]
    searchlist2=[]
    namepq=StringVar(rootpro)
    idpq=StringVar(rootpro)
    scnpq=StringVar(rootpro)
    manfacpq=StringVar(rootpro)
    cstpq=StringVar(rootpro)
    Label(rootpro,text="ENTER SOME DATA TO PROCEED WITH QUERY:").grid(row=3,column=0,columnspan=2)

    Label(rootpro,text="Product Name :").grid(row=4,column=0)
    Label(rootpro, text="Product id :").grid(row=5, column=0)
    Label(rootpro, text="Category :").grid(row=6, column=0)
    Label(rootpro, text="Manufacturer :").grid(row=7, column=0)
    Label(rootpro, text="Cost :").grid(row=8, column=0)

    Entry(rootpro,textvariable=namepq,width=50).grid(row=4,column=1)
    Entry(rootpro, textvariable=idpq,width=50).grid(row=5,column=1)
    Entry(rootpro, textvariable=scnpq,width=50).grid(row=6,column=1)
    Entry(rootpro, textvariable=manfacpq,width=50).grid(row=7,column=1)
    Entry(rootpro, textvariable=cstpq,width=50).grid(row=8,column=1)
    #Button(root,text="SEARCH",command=srchcq,font=('times',15, 'bold')).grid(row=8,columnspan=2)

    Button(rootpro,text="Search Records",command=searchpq,font=('times',17, 'bold')).grid(row=9,column=0,columnspan=2)

    rootpro.mainloop()
    pass
def searchpq():
    global searchlist,searchlist2
    global namepq,idpq,scnpq,manfacpq,cstpq

    if (namepq.get(),idpq.get(),scnpq.get(),manfacpq.get(),cstpq.get())==("","","","",""):
        tkMessageBox.showinfo(message="All boxes are empty  !!!")
    else:
        if scnpq.get() != "":
            searchtherecords(scnpq.get(), "category")
        # (namepq,idpq,scnpq,manfacpq,cstpq):
        if namepq.get()!="":
            searchtherecords(namepq.get(),"name")
        if manfacpq.get != "":
            searchtherecords(manfacpq.get(), "manufacturer")
        if idpq.get()!="":
            searchtherecords(idpq.get(),"proid")

        if cstpq.get() !="":
            searchtherecordscst(cstpq.get(),"cost")
        if searchlist==[] and searchlist2==[]:
            tkMessageBox.showinfo(message="No Records found")
        else:
            global rootpro
            rootpro.destroy()
            A=Tk()
            Label(A,text="These are the closest results resembling your queries(greater than 45% similarity):").grid(row=0,columnspan=6)
            Label(A,text="Product id",relief='ridge').grid(row=1,column=0)
            Label(A,text="Name",relief='ridge').grid(row=1,column=1)
            Label(A,text="Category",relief='ridge').grid(row=1,column=2)
            Label(A,text="Manufacturer",relief='ridge').grid(row=1,column=3)
            Label(A,text="Addqnty",relief='ridge').grid(row=1,column=4)
            Label(A,text="Cost",relief='ridge').grid(row=1,column=5)
            line=2
            for i in searchlist:
                Label(A, text=i[0]).grid(row=line, column=0)
                Label(A, text=i[2]).grid(row=line, column=1)
                Label(A, text=i[3]).grid(row=line, column=2)
                Label(A, text=i[4]).grid(row=line, column=3)
                Label(A, text=i[5]).grid(row=line, column=4)
                Label(A, text=i[6]).grid(row=line, column=5)
                line+=1
            Button(A,text="Main Menu").grid(row=line,column=0,columnspan=2)
            A.mainloop()
def searchtherecordscst(value,x):
    global searchlist
    a = sqlite3.connect("list_of_products.sqlite")
    df = pd.read_sql("select * from itemlist", a)
    v=int(value)
    for i in df[x].values.tolist():
        if v>int(i):
            if v-int(i)< 0.2*v:
                df2 = df.loc[df[x].isin([i])]
                for i2 in df2.values.tolist():
                    if i2 not in searchlist:
                        searchlist.append(i2)
        else:
            if int(i)-v<0.2*v:
                df2 = df.loc[df[x].isin([i])]
                for i2 in df2.values.tolist():
                    if i2 not in searchlist:
                        searchlist.append(i2)

def searchtherecords(value,x):
    a = sqlite3.connect("list_of_products.sqlite")
    df = pd.read_sql("select * from itemlist", a)
    global searchlist,searchlist2
    if value in df[x].values.tolist():
        df1=df.loc[  df[x].isin([value])   ]
        for i in df1.values.tolist():
            if i not in searchlist:
                searchlist.append(i)
    else:
        for i in df[x].values.tolist():
            if patrn(value,str(i))>0.45 :
                df2 = df.loc[df[x].isin([i])]
                for i2 in df2.values.tolist():
                    if i2 not in searchlist:
                        searchlist.append(i2)

###################################################################################$####$#$#$#$#$#$#$#$#$#$#$###$#
