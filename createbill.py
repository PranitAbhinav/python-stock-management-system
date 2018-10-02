import sqlite3
from Tkinter import *
import tkMessageBox
import pandas as pd
import barscanner
import win32api
import win32print
import random
import time
global a,billingsto,line,shoplist,q
q=[]
line=8
shoplist=[]
####################################################################################################################################
def scanit():
    global a,billingsto,line,shoplist,q
    scan=barscanner.barscan()
    if scan not in shoplist:
        printdetail(scan)
    else:
        tkMessageBox.showinfo('message',message="you already scanned this item\nTRY CHANGING IT'S QUANTITY")
list=sqlite3.connect('list_of_products.sqlite')
cur=list.cursor()
cur.execute("SELECT * FROM itemlist")
data=cur.fetchall()
rem=[]
for i in data:
    rem.append(i[1])
def printdetail(scan):
    global line
    if scan in rem:
        shoplist.append(scan)
        for i in data:
            if i[1]==scan:
                Label(billingsto,text=i[2]).grid(row=line,column=0)#name
                Label(billingsto, text=i[5]).grid(row=line, column=1)#qnty remain
                Label(billingsto, text=i[6]+"rs.").grid(row=line, column=2)#
                Label(billingsto, text=i[4]).grid(row=line, column=3)  #
                q.append((  i[0],i[1] ,i[2] ,i[4],i[6]   ,StringVar(billingsto)    ))#id,scan val,name,manufacr.,cost

                qtys = Entry(billingsto,textvariable=q[len(q)-1][5])
                qtys.grid(row=line, column=5)
                line = line + 1
                break
    else:
        tkMessageBox.showinfo('message',message="No Such Product!!")
####----------------------------------------------------------========================================------------------------------------------------
#$$$$$$$$========================================================          SAVE BILL            =======================================================
#########==============================================================================================================================================
def savebill():
    global billingsto
    billingsto.destroy()
    global name,variable,phno,ref
    a = sqlite3.connect('bills.db')
    cur = a.cursor()

    localtime = time.localtime(time.time())
    cur.execute('CREATE TABLE if not exists  billdetail (ref integer id,name text,cashmode text,phoneno integer,time string)')
    cur.execute('INSERT INTO billdetail (ref,name,cashmode,phoneno,time) VALUES(?,?,?,?,?)',(ref,name.get(),variable.get(),phno.get(),str(localtime[0:5])))
    a.commit()
    a.close()
    print name.get(),variable.get(),phno.get(),ref,str(localtime[0:5])
    for i in range(len(q)):
        a2 = sqlite3.connect('list.db')
        cur11 = a2.cursor()
        cur11.execute('CREATE TABLE if not exists  items (ref integer,proid integer,scan text,namepro text,manuf text,cost integer,quantitybought integer)')
        cur11.execute('INSERT INTO items (ref,proid,scan,namepro,manuf,cost,quantitybought) VALUES(?,?,?,?,?,?,?)',
                    ((ref),(q[i][0]) , q[i][1] , q[i][2],q[i][3], (q[i][4]), (q[i][5].get())))
        a2.commit()
        a2.close()
        print "======================================"
        print "NO.",i,":"
        print "id=",q[i][0]
        print "Scan val=",q[i][1]
        print "name=",q[i][2]
        print "manufacturer=",q[i][3]
        print "cost",q[i][4]
        print "qntity=",q[i][5].get()

        li2 = sqlite3.connect('list_of_products.sqlite')
        cur1 = li2.cursor()
        df = pd.read_sql("SELECT * FROM itemlist where proid=(?)", li2, params=((q[i][0] , )))

        preq = (int(df['addqnty'][0])) - int((q[i][5].get()))
        cur1.execute('''UPDATE itemlist SET addqnty = ? WHERE proid= ? ''', ((preq, q[i][0])))


        li2.commit()
        li2.close()



    li=sqlite3.connect('hi.db')
    curs=li.cursor()
    curs.execute('''UPDATE billref1 SET bref = ? WHERE i = ? ''',
                 (ref+1, 0))
    li.commit()
    li.close()
    import mainfile
    mainfile.show()
#=======================================================================================================================

def khali():
    print "no action available"

def billingitems():
    global c, cur, flag, t, name1, add, billingsto, n, lb1,a
    t = 0
    billingsto = Tk()
    #billingsto.geometry('620x500+0+0')
    billingsto.title('BILLING')
    Label(billingsto, text='-' * 48 + 'Billing' + '-' * 49).grid(row=0, column=0, columnspan=7, sticky='W')
    Label(billingsto, text='Enter Name: ').grid(row=1, column=0)
    global name,variable,phno,ref
    name=StringVar(billingsto)
    name1 = Entry(billingsto,textvariable=name)
    name1.grid(row=1, column=1)
    Label(billingsto, text="Bill Ref. code.: ").grid(row=2, column=0)

    a1 = sqlite3.connect('hi.db')
    cur = a1.cursor()
    cur.execute('SELECT * FROM billref1')
    ref=cur.fetchall()[0][1]
    a1.close()


    Label(billingsto,text=ref).grid(row=2, column=1)
    variable = StringVar(billingsto)
    variable.set("CASH")  # default value
    Label(billingsto, text="Cash Mode").grid(row=4, column=0)
    cashmode = OptionMenu(billingsto, variable, "Debit Card", "Credit Card", "CASH","Membership Points")
    cashmode.grid(row=4, column=1,columnspan=1)
    Label(billingsto, text="Phone number: ").grid(row=3, column=0)
    phno=StringVar(billingsto)
    phone = Entry(billingsto,textvariable=phno)
    phone.grid(row=3, column=1)

    Label(billingsto, text='-' * 115).grid(row=6, column=0, columnspan=7, sticky='W')
    Label(billingsto, text='Select Item', relief='ridge', width=15).grid(row=7, column=0)
    Label(billingsto, text='Qty_Remain', relief='ridge', width=10).grid(row=7, column=1)
    Label(billingsto, text='Cost', relief='ridge', width=4).grid(row=7, column=2)
    Label(billingsto, text='manufacturer', width=10, relief='ridge').grid(row=7, column=3)

    Label(billingsto, text='QUANTITY', width=20, relief='ridge').grid(row=7, column=5)


    Button(billingsto, width=15, text='scan',
           command=scanit).grid(row=1, column=6)

    Button(billingsto, width=15, text='Reset Bill',
           command=resetbill).grid(row=4, column=6)
    Button(billingsto, width=15, text='Main Menu',activebackground='blue',bg='red1',
           command=mainmenu).grid(row=10, column=6)
    Button(billingsto, width=15, text='Save Bill',
           command=savebill).grid(row=7, column=6)
    billingsto.mainloop()

def resetbill():
    global a, billingsto, line, shoplist, q
    q = []
    line = 8
    shoplist = []
    temp = []
    billingsto.destroy()
    billingitems()
def mainmenu():
    billingsto.destroy()
    import mainfile
    mainfile.show()
