from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image

import sqlite3
import pandas as pd
import time

global r
global flag
flag=1
global nameELv,pwordELv
def tick():
    global time1,temp3
    hr=int(time.strftime('%H'))
    time2 = time.strftime('%M:%S')
    if time2 != time1:
        time1 = time2
        if hr/12==0:
            clock.config(text="LOCAL TIME:\n"+str(hr%12)+':'+time2+"   AM")
        else:
            clock.config(text="LOCAL TIME:\n"+str(hr%12)+':'+time2+"   PM")
    if temp3==0:
        clock.after(200, tick)
    else:
        pass



def callf():
    import createbill
    hide()
    createbill.billingitems()
def khali():
    print "no action available"
def searchrecd():
    hide()
    import database1
    database1.searchrecord()
def loggedin():
    global w
    w = Tk()
    w.geometry("900x600+0+0")
    w.title("store billing system")

    menu_bar = Menu(w)
    w.config(menu=menu_bar)
    billing_menu = Menu(menu_bar,tearoff=0)
    HELP= Menu(menu_bar, tearoff=0)
    security=Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='File', menu=billing_menu)
    menu_bar.add_cascade(label='security', menu=security)


    security.add_command(label="Update password", command=chngpw)
    billing_menu.add_command(label="update product", command=updatepro)
    billing_menu.add_command(label="Delete Product", command=DELETESTOCK)



    lbl=Label(w,font=('arial',50,'italic'),text='XYZ STORES',fg='RED').grid(row=0,column=1)#87979
    global time1,clock,fr,temp3
    temp3=0

    time1 = ''
    clock = Label(w, font=('times', 20, 'bold'), bg='white')
    clock.grid(row=3,column=1,ipadx=50)
    tick()

    b1=Button(w,activebackground='LightSteelBlue3',bg='LightSteelBlue1',text='star making bills',command=callf,height=4,width=30).grid(row=2,column=0)
    b2=Button(w,activebackground='azure2',bg='LightSteelBlue1',text='introduce new product',command=adnw,width=30,height=4).grid(row=2,column=2)
    b3=Button(w,text='check stock',command=checkstock,width=30,height=4).grid(row=3,column=0)
    b4=Button(w,activebackground='azure2',text='know the product',command=knowpro,width=30,height=4).grid(row=3,column=2)
    b5=Button(w,activebackground='LightSteelBlue3',bg='LightSteelBlue1',text='search record',command=searchrecd,width=30,height=4).grid(row=4,column=0)
    b6=Button(w,activebackground='azure2',bg='LightSteelBlue1',text='perform queries',command=queries,width=30,height=4).grid(row=4,column=2)
    b7=Button(w,activebackground='LightSteelBlue3',bg='LightSteelBlue1',text='EXIT',command=exit,width=11,height=1,font=('arial','19','italic')).grid(row=5,column=1)

    w.mainloop()
#===================================================================     Queries           -----------------------------------------------------
def queries():
    hide()
    import Queries
    Queries.Query()

# =====================   CHANGE PASSWORD       ================================================================================================
def chngpw():
    #  curpw.execute('''CREATE TABLE if not exists passw
    #                   (id integer id,pw text)''')
    global np, npa, chn,w
    w.withdraw()
    chn=Tk()
    Label(chn,text='PLESAE CHANGE YOUR PASSWORD BELOW:').grid(row=0,columnspan=3)
    Label(chn, text='NEW PASSWORD:').grid(row=1,column=0)
    np=StringVar(chn)
    npa=StringVar(chn)
    np1=Entry(chn,textvariable=np,show="*").grid(row=1,column=1)

    Label(chn, text='Type again:').grid(row=2,column=0)
    np2=Entry(chn,textvariable=npa,show='*').grid(row=2,column=1)

    Button(chn,text='SET',command=func1,width='10').grid(row=4,column=1)
    chn.mainloop()
def func1():
    global chn,np,npa
    chn.destroy()
    if np.get()==npa.get():
        a = sqlite3.connect('hi.db')
        curpw = a.cursor()
        curpw.execute('''UPDATE passw SET pw = ? WHERE id = ? ''',(np.get(), 0))
        a.commit()
        a.close()
        tkMessageBox.showinfo(message='PASSWORD SUCCESFULLY UPDATED !!')
        w.deiconify()
    else:
        tkMessageBox.showinfo(message='FIELDS DO NOT MATCH')
        chngpw()
#####################################################              DELETE STOCK                 #####################################
def DELETESTOCK():
    global w,sto,delvar
    hide()
    sto=Tk()

    delvar=StringVar(sto)
    Label(sto,text="ENTER PRODUCT ID TO DELETE:").grid(row=0,column=0,columnspan=3)
    Entry(sto,textvariable=delvar).grid(row=0,column=4,columnspan=1)
    Button(sto,text="DELETE",command=dele).grid(row=0,column=5,columnspan=1)
    ref()
    Button(sto,text="Main menu",command=mm).grid(row=16)
    sto.mainloop()
def dele():
    global delvar,sto
    a = sqlite3.connect("list_of_products.sqlite")
    cur=a.cursor()
    df = pd.read_sql("select * from itemlist", a)
    print df['proid'].values.tolist()
    if int(delvar.get()) not in df['proid'].values.tolist():
        tkMessageBox.showinfo(message="NO Such Product")
    else:
        print delvar.get()
        cur.execute("DELETE FROM itemlist where proid=?",((     delvar.get()  , )))
        a.commit()
        cur.close()
        a.close()
        sto.destroy()
        DELETESTOCK()
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$           UPDATE PRODUCT            *************************************************



def updatepro():
    global w,sto,delvar
    hide()
    sto=Tk()

    delvar=StringVar(sto)
    Label(sto,text="ENTER PRODUCT ID TO UPDATE:").grid(row=0,column=0,columnspan=3)
    Entry(sto,textvariable=delvar).grid(row=0,column=4,columnspan=1)
    Button(sto,text="UPDATE",command=updtpr).grid(row=0,column=5,columnspan=1)
    ref()
    Button(sto,text="Main menu",command=mm).grid(row=16)
    sto.mainloop()

def updtpr():
    global delvar,sto
    a = sqlite3.connect("list_of_products.sqlite")
    cur=a.cursor()
    df = pd.read_sql("select * from itemlist", a)

    if int(delvar.get()) not in df['proid'].values.tolist():
        tkMessageBox.showinfo(message="NO Such Product")
    else:
        global tkn
        sto.destroy()
        tkn=Tk()
        global qn,cs
        qn=StringVar(tkn)
        cs=StringVar(tkn)
        Label(tkn,text="Enter new Quantity:").grid(row=1,column=0)
        Entry(tkn,textvariable=qn).grid(row=1,column=1)
        Label(tkn, text="Enter new cost:").grid(row=2,column=0)
        Entry(tkn,textvariable=cs).grid(row=2,column=1)
        Button(tkn,text="UPDATE",command=upd).grid(row=3,column=0)
        tkn.mainloop()
def upd():

    global qn, cs,delvar,tkn
    if qn.get()!="" and cs.get()!="":
        a = sqlite3.connect("list_of_products.sqlite")
        cur = a.cursor()
        cur.execute("UPDATE itemlist SET  addqnty= ? WHERE proid = ? ",(int(qn.get()),int(delvar.get())))
        cur.execute("UPDATE itemlist SET  cost= ? WHERE proid = ? ",(int(cs.get()),int(delvar.get())))
        a.commit()
        a.close()
        tkn.destroy()
        updatepro()
    else:
        tkMessageBox.showinfo(message="boxes are empty")

#$$$$$$$$$$$$$$$$$$$==========================================================================================================================
# ==============================================               ....CHECK STOCKS....                         ==================================
#=============================================================================================================================================
def show():
    global w
    w.deiconify()
def hide():
    global w
    w.withdraw()
def checkstock():
    global w,sto
    hide()
    sto=Tk()
    Label(sto,text="Welcome!!!Your Stocks are displayed here:").grid(row=0,columnspan=3)
    ref()
    Button(sto,text="Main menu",command=mm).grid(row=16)
    sto.mainloop()
def mm():
    global sto
    sto.destroy()
    show()
def ref():
    ''' Multilistbox to show all the data in database '''
    global sto, cur, c
    list = sqlite3.connect('list_of_products.sqlite')
    cur1 = list.cursor()
    cur1.execute('''SELECT * FROM itemlist''')
    tempfetch = cur1.fetchall()
    print tempfetch
    def scrollbarv(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)
    index = 0
    sc_bar = Scrollbar(orient='vertical', command=scrollbarv)
    lb0 = Listbox(sto, yscrollcommand=sc_bar.set,width=8)
    lb1 = Listbox(sto, yscrollcommand=sc_bar.set)
    lb2 = Listbox(sto, yscrollcommand=sc_bar.set)
    lb3 = Listbox(sto, yscrollcommand=sc_bar.set, width=17)
    lb4 = Listbox(sto, yscrollcommand=sc_bar.set, width=17)
    lb5 = Listbox(sto, yscrollcommand=sc_bar.set, width=20)
    lb6 = Listbox(sto, yscrollcommand=sc_bar.set, width=20)
    sc_bar.grid(row=15, column=6, sticky=N + S)
    Label(sto,text='id',relief='ridge').grid(row=14, column=0)
    Label(sto,text='Scan Value',relief='ridge').grid(row=14, column=1)
    Label(sto,text='Product Name',relief='ridge').grid(row=14, column=2)
    Label(sto,text='Category',relief='ridge').grid(row=14, column=3)
    Label(sto,text='Manufactured by',relief='ridge').grid(row=14, column=4)
    Label(sto,text='Quantity Left',relief='ridge').grid(row=14, column=5)
    Label(sto,text='Cost',relief='ridge').grid(row=14, column=6)

    lb0.grid(row=15, column=0)
    lb1.grid(row=15, column=1)
    lb2.grid(row=15, column=2)
    lb3.grid(row=15, column=3)
    lb4.grid(row=15, column=4)
    lb5.grid(row=15, column=5)
    lb6.grid(row=15, column=6)
    for i in tempfetch:
        index += 1
        lb0.insert(index, str(i[0]))
        lb1.insert(index, str(i[1]))
        lb2.insert(index, i[2])
        lb3.insert(index, i[3])
        lb4.insert(index, i[4])
        lb5.insert(index, i[5])
        lb6.insert(index, i[6])
    list.close()
###################################################     ..............ADDING NEW PRODUCT.................

def adnw():#ADDING NEW ITEMS TO GODOWN
    global temp3
    temp3=1
    hide()
    import additems
    additems.addnew()
################################################              know PRODUCTTTTTT                 #################################################################
def scanit():
    import barscanner
    global root2,scan,lab
    lab.destroy()
    scan=barscanner.barscan()
    photo001 = Image.open('imagescanned.PNG')

    resized = photo001.resize((70, 70), Image.ANTIALIAS)
    photo02 = ImageTk.PhotoImage(resized,master=root2)
    pin= Button(root2,image=photo02, height=80,width=80,command=scanned)
    pin.grid(row=1, column=1,rowspan=2)

    Label(root2,text='Click on the SCANNED button to know\nthe barcode value').grid(row=4,columnspan=2)
    root2.mainloop()
def scanned():
    global scan
    tkMessageBox.showinfo('scanneditem',message='THE SCAN RECIEVED IS:::>>>'+scan)
def knowpro():
    global root2,lab,scan,temp3,w
    temp3=1
    hide()
    root2=Tk()
    root2.geometry('318x145')
    scan=""
    b1=Button(root2, text="SCAN", command=scanit, height=2,width=30).grid(row=1, column=0)
    lab = Label(root2, text="No Scan available", fg='red')
    lab.grid(row=1, column=1)
    photo1 = Image.open('images_search.png')
    resized = photo1.resize((213,40), Image.ANTIALIAS)
    photo01 = ImageTk.PhotoImage(resized,master=root2)
    b2=Button(root2,image=photo01, command=search,height=40, width=213).grid(row=2, column=0)
    b3=Button(root2,text="EXIT",fg='red', command=exit,).grid(row=3, column=0)
    root2.mainloop()

def search():
    global scan
    if scan=='':
        tkMessageBox.showinfo('message',message="SCAN ITEM FIRST")
    else:
        list = sqlite3.connect('list_of_products.sqlite')
        cur1 = list.cursor()
        cur1.execute('''SELECT * FROM itemlist''')
        tempfetch=cur1.fetchall()
        l=[]
        for i in tempfetch:
            l.append(i[1])
        if scan not in l:
            tkMessageBox.showinfo('message', message="OOPS!!NO SUCH ITEM!!!!")
        else:
            for i in tempfetch:
                if i[1]==scan:
                    item=i[2]
                    manufac=i[4]
                    cst=i[6]
            tkMessageBox.showinfo('message', message="THE ITEM IS=>>"+item+"\nMANUFACTURED BY=>>"+manufac+"\nCOST=>>"+str(cst))
        list.close()
        root2.destroy()
        show()


######################################       LOGIN          ##################################################
def login():
    global nameEL
    global pwordEL  # More globals
    global rootA

    rootA = Tk()  # This now makes a new window.
    rootA.title('Login')  # This makes the window title 'login'
    rootA.geometry('400x400')
    intruction = Label(rootA, text='Please Login\n')  # More labels to tell us what they do
    intruction.grid(sticky=E)  # Blahdy Blah

    nameL = Label(rootA, text='Username: ')  # More labels
    pwordL = Label(rootA, text='Password: ')  # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)
    global nameELv,pwordELv
    nameELv = StringVar()
    pwordELv = StringVar()
    nameEL = Entry(rootA,textvariable=nameELv,width=30)  # The entry input
    pwordEL = Entry(rootA, show='*',textvariable=pwordELv,width=30)
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)
    global ltemp
    ltemp = Label(rootA, text="WELCOME PLEASE LOGIN TO CONTINUE !!!!!!", fg='blue2',font=('arial',10,'italic'))
    ltemp.grid(row=4,column=0,columnspan=3)
    loginB = Button(rootA, text='LOGIN',command=checkup,width=21,height=1)  # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(column=1,columnspan=2, sticky=W)

    exit = Button(rootA, text='EXIT', fg='red',command=rootA.destroy)  # This makes the deluser button. blah go to the deluser def.
    exit.grid(columnspan=2, sticky=W)
    img = Image.open('images.jpg')
    resized = img.resize((390, 260), Image.ANTIALIAS)
    photo1 = ImageTk.PhotoImage(resized)


    panel = Label(rootA, image=photo1)
    panel.grid(row=7,column=0,columnspan=3,rowspan=3,ipadx=3)
    rootA.mainloop()

def checkup():
    a = sqlite3.connect('hi.db')
    curpw = a.cursor()
    a.commit()
    curpw.execute("SELECT * FROM passw")
    t = curpw.fetchall()
    a.close()
    global rootA,nameELv,pwordELv
    if nameELv.get()=='admin' and pwordELv.get()==t[0][1]:
        rootA.destroy()
        loggedin()
    else:
        global ltemp
        tem=Label(rootA,text="Login Failed!!!",fg='red',font=('arial',10,'bold'))
        tem.grid(row=6,columnspan=3)

def setflag(value):
    if value==0:
        login()
    else:
        loggedin()
def logout():
    global w,clock,temp3
    temp3=1
    w.destroy()
    login()