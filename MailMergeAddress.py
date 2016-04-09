import usaddress
import collections
import csv
import sys
import tkinter
import tkFileDialog
import xlsxwriter
import pandas as pd
import numpy



if sys.version_info[0] < 3:
   import Tkinter as Tk
else:
   import tkinter as Tk


def browse_file():
    global fname
    fname = tkFileDialog.askopenfilenames(filetypes = (("Template files", "*.xlsx"), ("Template files", "*.xls")))
    print fname[0]
    print fname[0].rsplit('/',1)
    print fname[0].rsplit('/',1)[0]


root = Tk.Tk()
root.wm_title("Mail Merge File Select")
root.configure(background = 'blue')
broButton = Tk.Button(master = root, text = 'Browse', width = 6, command=browse_file, bg="white")
broButton.pack(side=Tk.LEFT, padx = 150, pady=100)
root.after(30000, lambda: root.destroy())
Tk.mainloop()


ls = ('First Name','Last Name','Fullname','Title','Company','Department','Address 1','Address 2','City','State','Zipcode','Country')

buffadd = pd.DataFrame(columns=ls)
usaddd = pd.DataFrame(columns=ls)
wrongaddress = pd.DataFrame(columns=ls)
wrongbuff = pd.DataFrame(columns=ls)








def addresscheck(df):
    for index, row in df.iterrows():
        addressstring = (row[1]+' '+ row[2]+' ' + row[4]+' ' + row[5])
        addresscheck = usaddress.tag(addressstring)
        if addresscheck[1] != 'Ambiguous':
            if addressstring.find('University at Buffalo') != -1:
                buffadd.loc[len(buffadd)]=df.iloc[index]
            else:
                usaddd.loc[len(usadd)]= df.iloc(index)
        else:
            if addressstring.find("University at Buffalo") != -1:
                wrongbuff.loc[len(wrongbuff)] = df.iloc(index)
            else:
                wrongaddress.loc[len(wrongaddress)] = df.iloc(index)





