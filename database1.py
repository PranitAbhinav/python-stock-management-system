from Tkinter import *
import tkMessageBox
import sqlite3
def searchrecord():
    global w,k
    k=Tk()
    Label(k,text='ENTER bill ref. code to open bill:').grid(row=0)
    w=StringVar(k)
    Entry(k,textvariable=w).grid(row=1)
    Button(k,text="GO",width=10,command=lambda :srch(w.get())).grid(row=2)
    k.mainloop()
def srch(val):
    global w
    a = sqlite3.connect('bills.db')
    cur = a.cursor()
    cur.execute('SELECT * FROM billdetail where ref=(?)', ((val)))
    za=cur.fetchall()
    print za
    a.close()
    if za==[]:

        tkMessageBox.showinfo(message='no such bill !')
        k.destroy()
        import mainfile
        mainfile.show()
    else:
        k.destroy()
        z=za[0]
        global new
        new=Tk()
        Label(new,text="Ref code :").grid(row=0,column=0)
        Label(new,text=str(z[0])).grid(row=0,column=1)

        Label(new, text="Customer name :").grid(row=1, column=0)
        Label(new, text=str(z[1])).grid(row=1, column=1)

        Label(new, text="Payment mode :").grid(row=2, column=0)
        Label(new, text=str(z[2])).grid(row=2, column=1)

        Label(new, text="phonenumber :").grid(row=3, column=0)
        Label(new, text=str(z[3])).grid(row=3, column=1)
        x=z[4][1:-1].split(", ")
        Label(new, text="Date :").grid(row=4, column=0)
        Label(new, text=x[2]+"/"+x[1]+"/"+x[0]).grid(row=4, column=1)

        Label(new, text="Time :").grid(row=5, column=0)
        Label(new, text=x[3]+":"+x[4] ).grid(row=5, column=1)

        def scrollbarv(*args):
            lb1.yview(*args)
            lb2.yview(*args)
            lb3.yview(*args)
            lb4.yview(*args)
            lb5.yview(*args)
            lb6.yview(*args)
        sto=new
        index = 0
        sc_bar = Scrollbar(orient='vertical', command=scrollbarv)
        lb1 = Listbox(sto, yscrollcommand=sc_bar.set)
        lb3 = Listbox(sto, yscrollcommand=sc_bar.set, width=17)
        lb4 = Listbox(sto, yscrollcommand=sc_bar.set, width=17)
        lb5 = Listbox(sto, yscrollcommand=sc_bar.set, width=20)
        lb6 = Listbox(sto, yscrollcommand=sc_bar.set, width=20)
        sc_bar.grid(row=15, column=6, sticky=N + S)
        Label(sto, text='Product id',relief='ridge').grid(row=14, column=0)
        Label(sto, text='item name',relief='ridge').grid(row=14, column=1)
        Label(sto, text='manufacturer',relief='ridge').grid(row=14, column=2)
        Label(sto, text='cost',relief='ridge').grid(row=14, column=3)
        Label(sto, text='Quantity',relief='ridge').grid(row=14, column=4)

        lb1.grid(row=15, column=0)
        lb3.grid(row=15, column=1)
        lb4.grid(row=15, column=2)
        lb5.grid(row=15, column=3)
        lb6.grid(row=15, column=4)
        a2 = sqlite3.connect('list.db')
        cur21 = a2.cursor()
        cur21.execute('SELECT * FROM items where ref=?' ,str(z[0]))
        te= cur21.fetchall()
        print te
        bill=0
        for i in te:
            index += 1
            lb1.insert(index, str(i[1]))
            lb3.insert(index, i[3])
            lb4.insert(index, i[4])
            lb5.insert(index, i[5])
            lb6.insert(index, i[6])
            bill+=(i[6]*i[5])
        Label(sto,text ="TOTAL BILL=",font=('times',15,"italic")).grid(row=16,column=3)
        Label(sto,text =str(bill)+" Rs.",font=('times',15,"bold")).grid(row=16,column=4)
        Button(sto,text="MAIN MENU",fg='red',command=mmm).grid(row=16,column=0)
        a2.close()

        new.mainloop()

def mmm():
    global new
    new.destroy()
    import mainfile
    mainfile.show()