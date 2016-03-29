import usaddress
import collections
import csv
import sys
import tkinter
import tkFileDialog
import xlsxwriter


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




buffaloadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Buffalo Addresses.xlsx')
buffsheet = buffaloadd.add_worksheet()
usadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/US addresses.xlsx')
ussheet = usadd.add_worksheet()
wrongadd = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Wrong Addresses.xlsx')
wrongsheet = wrongadd.add_worksheet()
wrongbuffalo = xlsxwriter.Workbook(fname[0].rsplit('/',1)[0] + '/Wrong Buffalo Addresses.xlsx')
wrongbuffsheet = wrongbuffalo.add_worksheet()

buffsheet.write('A1',"Name")
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
wrongbuffsheet.set_column('E:E',15)





us_dict = collections.OrderedDict()
def addresscheck(string):
    us_dict = usaddress.tag(string)
    if(us_dict[1] != 'Ambiguous'):
        if usaddress.tag(string)[0]['StreetName'].find("University at Buffalo") != -1:
            buffsheet.write('A2', us_dict[0]['Recipient'])
            buffsheet.write('B2', us_dict[0]['AddressNumber'] + ' '+  us_dict[0]['StreetNamePreDirectional']+ ' '+ us_dict[0]['StreetName'] + ' '+  us_dict[0]['StreetNamePostType'] + ' ' + us_dict[0]['OccupancyType'] + ' ' +  us_dict[0]['OccupancyIdentifier']  )
            buffsheet.write('C2', us_dict[0]['PlaceName'])
            buffsheet.write('D2', us_dict[0]['StateName'])
            buffsheet.write('E2', us_dict[0]['ZipCode'])
        else:
            ussheet.write('A2', us_dict[0]['Recipient'])
            ussheet.write('B2', us_dict[0]['AddressNumber'] + ' '+  us_dict[0]['StreetNamePreDirectional']+ ' '+ us_dict[0]['StreetName'] + ' '+  us_dict[0]['StreetNamePostType'] + ' ' + us_dict[0]['OccupancyType'] + ' ' +  us_dict[0]['OccupancyIdentifier']  )
            ussheet.write('C2', us_dict[0]['PlaceName'])
            ussheet.write('D2', us_dict[0]['StateName'])
            ussheet.write('E2', us_dict[0]['ZipCode'])
    else:
        if string.find("University at Buffalo") != -1:
            wrongbuffsheet.write('A2',string)
        else:
               wrongsheet.write('A2', string)


    #print us_dict
    #print us_dict[1]
    '''print us_dict[0]['Recipient']
    print us_dict[0]['AddressNumber']
    print us_dict[0]['StreetNamePreDirectional']
    print us_dict[0]['StreetName']
    print us_dict[0]['StreetNamePostType']
    print us_dict[0]['OccupancyType']
    print us_dict[0]['OccupancyIdentifier']
    print us_dict[0]['PlaceName']
    print us_dict[0]['StateName']
    print us_dict[0]['ZipCode']'''


addresscheck("Brandon Mendez 383 E 195th st apt 1D Bronx NY 10458")
addresscheck("Brandon Mendez UNIVERSITY AT BUFFALO	BUFFALO	NY	14260")
addresscheck("Brandon Mendez E 195th st apt 1D  NY 10458")
addresscheck("Brandon Mendez University at Buffalo NY")


buffaloadd.close()
usadd.close()
wrongadd.close()
wrongbuffalo.close()