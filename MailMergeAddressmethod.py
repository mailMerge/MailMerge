import usaddress
import collections
import csv
import sys
import tkinter
import tkFileDialog
import xlsxwriter
import pandas as pd
import numpy
import time


ls = ('First Name','Last Name','Fullname','Title','Company','Department','Address 1','Address 2','City','State','Zipcode','Country')

buffadd = pd.DataFrame(columns=ls)
usadd = pd.DataFrame(columns=ls)
wrongaddress = pd.DataFrame(columns=ls)
wrongbuff = pd.DataFrame(columns=ls)
testdf = pd.read_excel('C:/Users/Brandon/Documents/School/Mail Merge/test.xlsx')


testdf = testdf.drop_duplicates(subset=['Address 1', 'Address 2', 'City', 'State', 'Zipcode'])


def addresscheck(df):
    for index, row in df.iterrows():
        addressstring = (unicode(row['Address 1'])+' '+ unicode(row['Address 2'])+' ' + unicode(row['City'])+' ' + unicode(row['State']) + ' ' + unicode(row['Zipcode']))
        try:
            addresscheck = usaddress.tag(addressstring)
        except usaddress.RepeatedLabelError:
            wrongaddress.loc[len(wrongaddress)] = df.iloc[index]

        if addresscheck[1] != 'Ambiguous':
            if addressstring.find('14261') == -1 and addressstring.find('14260') == -1 and addressstring.find('Clement') == -1 and addressstring.find('Goodyear') == -1:
                usadd.loc[len(usadd)]= df.iloc[index]

        else:
            if addressstring.find('14261') == -1 and addressstring.find('14260') == -1 and addressstring.find('Clement') == -1 and addressstring.find('Goodyear') == -1:
                wrongaddress.loc[len(wrongaddress)] = df.iloc[index]




start = time.time()
addresscheck(testdf)
end = time.time()
print end-start
