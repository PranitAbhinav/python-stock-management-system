import sqlite3
from Tkinter import *
import pandas as pd
li2 = sqlite3.connect('list_of_products.sqlite')
cur1 = li2.cursor()
i=0
q=[[1,0,0,0,0,5]]
df = pd.read_sql("SELECT * FROM itemlist where proid=(?)", li2, params=(( q[i][0] , )))
print df
preq = (int(df['addqnty'][0])) - (q[i][5])
cur1.execute('''UPDATE itemlist SET addqnty = ? WHERE proid= ? ''', (preq, q[i][0]))
df = pd.read_sql("SELECT * FROM itemlist where proid=(?)", li2, params=([ q[i][0]   ]))
print df
