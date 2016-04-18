import pandas as pd
import numpy as np
import glob
import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
from argparse import ArgumentParser
from gooey import Gooey, GooeyParser



## --- setup dataframes
ls = ('First Name','Last Name','Fullname','Title','Company','Department','Address 1','Address 2','City','State','Zipcode','Country')
buffadd = pd.DataFrame(columns=ls)
usadd = pd.DataFrame(columns=ls)
wrongaddress = pd.DataFrame(columns=ls)
wrongbuff = pd.DataFrame(columns=ls)

output_df = {'buffaloAddress.xlsx':buffadd,'usAddress.xlsx':usadd,'wrongAddress.xlsx':wrongaddress,'wrongBuffaloAddress.xlsx':wrongbuff}

@Gooey(program_name="Mail Merge")
def parse_args():
    """ Use GooeyParser to build up the arguments we will use in our script
    Save the arguments in a default json file so that we can retrieve them
    every time we run the script.
    """
    
    stored_args = {}
    # get the script name without the extension & use it to build up
    # the json filename
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    # Read in the prior arguments as a dictionary
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)
    parser = GooeyParser(description='Mail Merge')
    parser.add_argument('data_directory',
                        action='store',
                        default=stored_args.get('data_directory'),
                        widget='DirChooser',
                        help="Source directory that contains Excel files")
    
    parser.add_argument('output_directory',
                        action='store',
                        widget='DirChooser',
                        default=stored_args.get('output_directory'),
                        help="Output directory to save merged files")

    #parser.add_argument("FileSaver", help="Name the output file you want to process", widget="FileSaver")
    #parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite output file (if present)")
    #parser.add_argument("-s", "--sheets", action="store_true", help="Would you like to ignore multiple sheets?")


    args = parser.parse_args()
    # Store the values of the arguments so we have them next time we run
    with open(args_file, 'w') as data_file:
        # Using vars(args) returns the data as a dictionary
        json.dump(vars(args), data_file)
    return args



def combine_files(src_directory):
    """ Read in all of the xlsx files apply functions and combine into 1
    combined DataFrame
    """
    all_data = pd.DataFrame()

    filelist = []
    fileTypes = ['*.xls', '*.xlsx','*.xlsm','*XLSX']
    for ftype in fileTypes:
        filelist.extend(glob.glob(src_directory+ftype))

    for f in filelist:
        for sheet in pd.ExcelFile(f).sheet_names:
            df = pd.read_excel(f,sheet)
            df = rename_columns(df)
            all_data = all_data.append(df, ignore_index=True)

    all_data.reset_index(drop=True)
    return all_data

#def dedupe():


def save_results(dataFile, output):
    """ Perform a summary of the data and save the data as an excel file
    """
    # extension = '.xlsx'
    # if filename.lower().endswith('.xlsx'):
    #     output_file = os.path.join(output, filename)
    # else:
    #     output_file = os.path.join(output, filename+extension)
    for key, value in output_df.iteritems():
        output_file = os.path.join(output, key)
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
        value.to_excel(writer)
        writer.save()

#-------------------------------------------------------------------------------------#
# Check address  return 4 more dataframes 

def addresscheck(df):
    for index, row in df.iterrows():
        addressstring = (row[1]+' '+ row[2]+' ' + row[4]+' ' + row[5])
        addresscheck = usaddress.tag(addressstring)
        if addresscheck[1] != 'Ambiguous':
            if addressstring.find('University at Buffalo') != -1:
                buffadd.loc[len(buffadd)]=df.iloc[index]
            else:
                usadd.loc[len(usadd)]= df.iloc[index]
        else:
            if addressstring.find("University at Buffalo") != -1:
                wrongbuff.loc[len(wrongbuff)] = df.iloc[index]
            else:
                wrongaddress.loc[len(wrongaddress)] = df.iloc[index]


#-------------------------------------------------------------------------------------#
# Mail Merge 

def guess_column_names(columnname):
    ''' An attempt to standardize and rename column headers for manipulation later.
        Input: column name (String)
        Output: Corrected name (String)
    '''    
    #list of possible "correct" column headers 
    correct_headers = ['First Name', 'Last Name','Fullname','Student Name','Job Title', 'Title','ID',
                       'Institution','School','Company','Company Name1','Company Name2','Organization Name','Department','Division',
                       'Email Address','Street Address','Street 1','Dorm Address 1','Dorm Address 2','Dorm Address 3',
                       'Dorm Address 4','Address 1','Street 2','Address 2','Address','Street 3','Address 3','Street 4','Address 4',
                       'Work Street 1','Work Street 2','Work Street 2','Work Street 3','Work Street 4',
                       'Zipcode','Home Zipcode','Work_City','Dorm Postalplus4','HOME_FOREIGN_CITYZIP','WORK_FOREIGN_CITYZIP','Work_State','Work_Country',
                       'Postal','City','County','State','Country']
    
    # if column is exact match return name
    if columnname in correct_headers:  # might want to make this a dict for O(1) lookups
        return columnname#, 100
    
    # if column name is longer than 20 characters, return best quess based on last 15 characters
    if len(columnname) > 20:
        new_name, score = process.extractOne(columnname[-15:], correct_headers) 
        return new_name#, score
    
    # for all others, 
    else:
        new_name, score = process.extractOne(columnname, correct_headers)
        
    #if score > 80, return new_name 
    if score < 80:
        # returns orginal name if match is bad
        return columnname#, score
    else:
        return new_name#, score

def unique_columns(df_columns):
    ''' Columns with same name get numbered to avoid duplication
        Input: list of columns
        Output: list of columns with appended numbers 
    '''
    seen = set()
    for col in df_columns:
        append = 1 
        newitem = col

        while newitem in seen:
            append += 1
            newitem = "{} {}".format(col, append)

        yield newitem
        seen.add(newitem)

def drop_columns(df):
    ''' Columns of the dataframe are dropped if they are not in the list below '''
    
    # If names don't match this list drop them from dataframe
    headers = ['First Name','Last Name','Fullname','Title',
               'Company','Department',
               'Address 1','Address 2',
               'City','State','Zipcode','Country']
    
    cols = [col for col in df.columns if col not in headers]
    #print cols
    df.drop(cols, axis=1, inplace=True)
    #print 'Drop: ',df.columns
    return df

def reorder_columns(dataframe, seq):
    '''Takes a dataframe and a sequence of columns names,
       returns dataframe with seq as first columns. If seq contains columns 
       that aren't in the dataframe then the columns are created with Nan values. 
    '''
    cols = seq[:]
    for x in dataframe.columns:
        if x not in cols:
             cols.append(x)
            
    for x in cols:
        if x not in dataframe.columns: #If column from seq is not in df, 
            dataframe[x]= np.nan       #create a new column filled with Nan
    
    return dataframe[cols]


def rename_columns(df):
    # List of New "corrected" column names
    new_col = [guess_column_names(col) for col in df.columns]
    
    #Set df columns equal to "corrected" columns 
    df.columns = new_col
    #print 'Corrected: ',df.columns
    
    # Rename Columns 
    df.rename(columns={'School':'Department',
                       'Institution':'Company',
                       'Organization':'Company',
                       'Organization Name':'Company',
                       'Street Address':'Street 1',
                       'Division':'Department',
                       'Postal':'Zipcode',
                       'Zip':'Zipcode',
                       'Home Zipcode':'Zipcode',
                       'Street 1':'Address 1',
                       'Street 2':'Address 2',
                       'Street 3':'Address 3',
                       'PERSON_NAME':'Fullname',
                       'Student Name':'Fullname'  #???
                       
                      }, inplace=True)
        
    #print 'Rename: ',df.columns
    
    #Call nameConcate here
    
    
    # Create unique versions of Columns to avoid issues with pandas 
    df.columns = list(unique_columns(df.columns))
    #print 'Unique: ',df.columns
    
    # Drop columns not needed 
    df = drop_columns(df)
    #print 'Drop: ',df.columns
    
    # Reorder Columns in df 
    df = reorder_columns(df,['First Name','Last Name','Fullname','Title','Company','Department','Address 1','Address 2','City','State','Zipcode','Country'])
    #print 'Reorder: ', df.columns
    
    return df

# def concatdf(dflist):
#     # takes in list of dataframes and concatenates them all together into one df
#     alldf = pd.concat(dflist)
#     alldf = alldf.reset_index(drop=True)
#     return alldf

# -------------------------------------------------------------------------------#

if __name__ == '__main__':
    conf = parse_args()
    print("Reading files and combining")
    all_df = combine_files(conf.data_directory)
    print("Saving data")
    save_results(all_df, conf.output_directory)
    print("Done")

