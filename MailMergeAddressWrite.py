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




'''buffaloadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Buffalo Addresses.xlsx')
buffsheet = buffaloadd.add_worksheet()
usadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/US addresses.xlsx')
ussheet = usadd.add_worksheet()
wrongadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Wrong Addresses.xlsx')
wrongsheet = wrongadd.add_worksheet()
wrongbuffalo = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Wrong Buffalo Addresses.xlsx')
wrongbuffsheet = wrongbuffalo.add_worksheet()'''


ls = ('Name','Address','City','State','ZipCode')
buffadd = pd.DataFrame(columns=ls)
usaddd = pd.DataFrame(columns=ls)
wrongaddress = pd.DataFrame(columns=ls)
wrongbuff = pd.DataFrame(columns=ls)


'''buffsheet.write('A1',"Name")
buffsheet.write('B1',"Address")
buffsheet.write('C1', "City")
buffsheet.write('D1' ,"State")
buffsheet.write('E1',"ZipCode" )
buffsheet.set_column('A:A',25)
buffsheet.set_column('B:B',40)
buffsheet.set_column('C:C',20)
buffsheet.set_column('D:D',15)
buffsheet.set_column('E:E',15)

ussheet.write('A1',"Name")
ussheet.write('B1',"Address")
ussheet.write('C1', "City")
ussheet.write('D1' ,"State")
ussheet.write('E1',"ZipCode" )
ussheet.set_column('A:A',25)
ussheet.set_column('B:B',40)
ussheet.set_column('C:C',20)
ussheet.set_column('D:D',15)
ussheet.set_column('E:E',15)

wrongsheet.write('A1',"Name")
wrongsheet.write('B1',"Address")
wrongsheet.write('C1', "City")
wrongsheet.write('D1' ,"State")
wrongsheet.write('E1',"ZipCode" )
wrongsheet.set_column('A:A',25)
wrongsheet.set_column('B:B',40)
wrongsheet.set_column('C:C',20)
wrongsheet.set_column('D:D',15)
wrongsheet.set_column('E:E',15)


wrongbuffsheet.write('A1',"Name")
wrongbuffsheet.write('B1',"Address")
wrongbuffsheet.write('C1', "City")
wrongbuffsheet.write('D1' ,"State")
wrongbuffsheet.write('E1',"ZipCode" )
wrongbuffsheet.set_column('A:A',25)
wrongbuffsheet.set_column('B:B',40)
wrongbuffsheet.set_column('C:C',20)
wrongbuffsheet.set_column('D:D',15)
wrongbuffsheet.set_column('E:E',15)'''






def addresscheck(string):
    global usdic
    usdic = dict(us_dict = usaddress.tag(string))
    usdic['us_dict'][0]['Recipient'] = 'Joe'
    print(usdic['us_dict'][0]['Recipient'])
    if( 'Ambiguous' in usdic['us_dict'][0]) == False:
        if(('StreetNamePreDirectional') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StreetNamePreDirectional'] = ' '
        if(('StreetNamePostType') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StreetNamePostType'] = ' '
        if(('OccupancyType') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['OccupancyType'] = ' '
        if(('OccupancyIdentifier') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['OccupancyIdentifier'] = ' '

        if usaddress.tag(string)[0]['StreetName'].find("University at Buffalo") != -1:
           buffadd.loc[0]= [ usdic['us_dict'][0]['Recipient'],(usdic['us_dict'][0]['AddressNumber'] + ' '+  usdic['us_dict'][0]['StreetNamePreDirectional']+ ' '+ usdic['us_dict'][0]['StreetName'] + ' '+  usdic['us_dict'][0]['StreetNamePostType'] + ' ' + usdic['us_dict'][0]['OccupancyType'] + ' ' +  usdic['us_dict'][0]['OccupancyIdentifier'] ) , usdic['us_dict'][0]['PlaceName'] , usdic['us_dict'][0]['StateName'], usdic['us_dict'][0]['ZipCode']]
        else:
            usaddd.loc[0]= [ usdic['us_dict'][0]['Recipient'],(usdic['us_dict'][0]['AddressNumber'] + ' '+  usdic['us_dict'][0]['StreetNamePreDirectional']+ ' '+ usdic['us_dict'][0]['StreetName'] + ' '+  usdic['us_dict'][0]['StreetNamePostType'] + ' ' + usdic['us_dict'][0]['OccupancyType'] + ' ' +  usdic['us_dict'][0]['OccupancyIdentifier'] ) , usdic['us_dict'][0]['PlaceName'] , usdic['us_dict'][0]['StateName'], usdic['us_dict'][0]['ZipCode']]

    else:
        if (('Recipient')in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['Recpipient'] = 'N/A'
        if(('AddressNumber')in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['AddressNumber'] = 'N/A'
        if(('StreetNamePreDirectional') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StreetNamePreDirectional'] = ' '
        if(('StreetName') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StreetName'] = 'N/A'
        if(('StreetNamePostType') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StreetNamePostType'] = ' '
        if(('OccupancyType') in usdic['us_dict'][0]) == False:
            usdic['us_dict']['OccupancyType'] = ' '
        if(('OccupancyIdentifier') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['OccupancyIdentifier'] = ' '
        if(('PlaceName') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['PlaceName'] = 'N/A'
        if (('StateName') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['StateName'] = 'N/A'
        if (('ZipCode') in usdic['us_dict'][0]) == False:
            usdic['us_dict'][0]['ZipCode'] = 'N/A'


        if string.find("University at Buffalo") != -1:
            wrongbuff.loc[0]= [ usdic['us_dict'][0]['Recipient'],(usdic['us_dict'][0]['AddressNumber'] + ' '+  usdic['us_dict'][0]['StreetNamePreDirectional']+ ' '+ usdic['us_dict'][0]['StreetName'] + ' '+  usdic['us_dict'][0]['StreetNamePostType'] + ' ' + usdic['us_dict'][0]['OccupancyType'] + ' ' +  usdic['us_dict'][0]['OccupancyIdentifier'] ) , usdic['us_dict'][0]['PlaceName'] , usdic['us_dict'][0]['StateName'], usdic['us_dict'][0]['ZipCode']]
        else:
            wrongaddress.loc[0]= [ usdic['us_dict'][0]['Recipient'],(usdic['us_dict'][0]['AddressNumber'] + ' '+  usdic['us_dict'][0]['StreetNamePreDirectional']+ ' '+ usdic['us_dict'][0]['StreetName'] + ' '+  usdic['us_dict'][0]['StreetNamePostType'] + ' ' + usdic['us_dict'][0]['OccupancyType'] + ' ' +  usdic['us_dict'][0]['OccupancyIdentifier'] ) , usdic['us_dict'][0]['PlaceName'] , usdic['us_dict'][0]['StateName'], usdic['us_dict'][0]['ZipCode']]



addresscheck("Brandon Mendez 383 E 195TH ST APT 1D Bronx NY 10458")
#buffadd.loc[1] = ['Brandon Mendez','383 E 195th ST Apt 1D','Bronx','NY','10458']



'''buffaloadd.close()
usadd.close()
wrongbuffalo.close()
wrongadd.close()'''