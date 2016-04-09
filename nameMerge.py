
import os 
import pandas as pd

path ='/home/jpack/workspace/mailMerge/Data/Greater Buffalo Business partners and ECI.xlsx'

class nameMerge:
    def __init__(self, path):
        df = pd.read_excel(path)
        self.header = list(df)
        #assuming the name of "name column" is known
        df1 = df[['Firstname','Lastname']]
        self.col1 = df1.as_matrix(columns=None);
        # ^convert column to array

    # if header contains first name or last name column, do nothing.
    def isDone(self):
        for s in self.header:
            if 'FullName' in s.lower():
                return True
            else: return False

    # if name column haven't been splited, find the name column
    # cuz we have already knew the column must be name column, no need for "tag"
    def nameMerge(self):
        if self.isDone() is False:
            nameList =[]
            for name in self.col1:
                first = name[0]
                last = name[1]
                #last, first
                full = last +", "+first
                nameList.append(full)

            return nameList

# to get a fullname list :
# fullnameLIst = nameMerge(path).nameMerge()