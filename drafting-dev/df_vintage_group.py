#taken from submission homework not yet adapated
#previously, created plots, but does not format them like in ipython

import pandas as pd
import datetime as dt
import numpy as np
import matplotlib

"""
Psydo Code:

collect data from file 

organize the file into series

check the math applied to series

built the series into small dataframes, indexed on loan number

#VINTAGE - seed data created
#LN COUNT - 
#UPB TOTAL - seed data created
#UPB AVERAGE - seed data created
#BRW FICO - seed data crated
#CO-BWR FICO - deed data created
#LTV RATIO - seed date crated
#CLTV RATIO - seed data crated
#DTI - seed data crated
#INTEREST RATE - seed data created

"""

"""
developer notes 

to_csv
Write DataFrame to a comma-separated values (csv) file.
read_csv
Read a comma-separated values (csv) file into DataFrame.
read_fwf
Read a table of fixed-width formatted lines into DataFrame.

DataFrame.reset_index
Opposite of set_index.
DataFrame.reindex
Change to new indices or expand indices.
DataFrame.reindex_like
Change to same indices as other DataFrame.

"""


class GetData():

    def __init__(self):
        # VINTAGE
        # LN COUNT
        # UPB TOTAL
        # UPB AVERAGE
        # BRW FICO
        # CO-BWR FICO
        # LTV RATIO
        # CLTV RATIO
        # DTI
        # INTEREST RATE
        pass


    def files_to_df(self, fname):
        #acq_header_file = pd.read_csv("header_aquisition_file.txt", sep=",")
        #print("headers file", acq_header_file.head())

        #columns = acq_header_file["Field Name"]
        #print("headers", columns)

        #index = 'LOAN IDENTIFIER'
        #index_col = index
        filter_columns = ['LOAN IDENTIFIER', 'ORIGINAL INTEREST RATE','ORIGINAL UPB',
                           'ORIGINATION DATE', 'ORIGINAL LOAN-TO-VALUE (LTV)','ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)','ORIGINAL DEBT TO INCOME RATIO', 'BORROWER CREDIT SCORE AT ORIGINATION','CO-BORROWER CREDIT SCORE AT ORIGINATION', 'SOURCE']

        #TO FILTER FOR SPEED, nrows=1000, FILTERED FOR 1000 ROWS, TURN THAT OFF FOR FINAL SUBMISSION
        df = pd.read_csv(fname, sep = ",",usecols=filter_columns, index_col=False, infer_datetime_format=True,)
        print(df.head())
        print(df.shape)
        print(df.columns)

        return df


    def df_to_files(self, df_name, fname):

        df_name.to_csv(fname, sep=',')

        return


class DataTransformations():

    def transformations(self, df_name):
        vintage_yr = DataTransformations.vintage(df_name, 'ORIGINATION DATE', 'VINTAGE') #created for group by
        ln_count = DataTransformations.count(df_name, 'LOAN IDENTIFIER', 'LOAN COUNT')  #created for loan count
        print("file loan count",df_name['LOAN IDENTIFIER'].count()) #develoepr check
        print('rule loan count', df_name['LOAN COUNT'].sum())  #developer check
        print('total upb', df_name['ORIGINAL UPB'].sum()) #developer check
        drop = ['ORIGINATION DATE','LOAN IDENTIFIER', 'SOURCE']  #finished with this column
        df_name1 = df_name.drop(drop, axis = 1)  #finished with this field after creating VINTAGE
        return df_name1

    def vintage(x, y, z):
        x[z] = pd.DatetimeIndex(x[str(y)]).year  #convert original file data to date format, get just year
        return

    def count(x, y, z): #look for a valid loan number, if present, then loan count is 1
        if x[y].notna:
            x[z] = 1
        else:
            x[z] = 0
        return


class VintageSummary():

    def call_summarization(self, df):
        Vintage = df
        byVintageWA = Vintage.groupby('VINTAGE').apply(VintageSummary.wa_upb_group)
        # print(byVintageWA) #developer check
        byVintageSum = Vintage.groupby('VINTAGE').apply(VintageSummary.sum_group)
        # print(byVintageSum) #developer check
        byVintageAvg = Vintage.groupby('VINTAGE').apply(VintageSummary.avg_group)
        # print(byVintageAvg) #developer check
        byVintage = pd.concat([byVintageSum, byVintageAvg, byVintageWA], axis=1)
        print(byVintage)
        return byVintage


    def wa_upb_group(group):
        group['Int Rate WA'] = round((group['ORIGINAL INTEREST RATE'] * group['ORIGINAL UPB']).sum()/group['ORIGINAL UPB'].sum(),1)
        group['BRW FICO WA'] = round((group['BORROWER CREDIT SCORE AT ORIGINATION'] * group['ORIGINAL UPB']).sum() / group['ORIGINAL UPB'].sum(),0)
        group['CO BRW FICO WA'] = round((group['CO-BORROWER CREDIT SCORE AT ORIGINATION'] * group['ORIGINAL UPB']).sum() / group['ORIGINAL UPB'].sum(),0)
        group['LTV WA'] = round((group['ORIGINAL LOAN-TO-VALUE (LTV)'] * group['ORIGINAL UPB']).sum() / group['ORIGINAL UPB'].sum(),1)
        group['CLTV WA'] = round((group['ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'] * group['ORIGINAL UPB']).sum() / group['ORIGINAL UPB'].sum(),1)
        group['DTI WA'] = round((group['ORIGINAL DEBT TO INCOME RATIO'] * group['ORIGINAL UPB']).sum() / group['ORIGINAL UPB'].sum(),1)
        drop_2 = ['ORIGINAL INTEREST RATE','BORROWER CREDIT SCORE AT ORIGINATION','ORIGINAL UPB', 'VINTAGE','LOAN COUNT', 'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)','ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        group1 = group.drop(drop_2, axis = 1)
        return group1.mean()

    def sum_group(group):
        group['Total UPB'] = round(group['ORIGINAL UPB'],0)
        group['Loan Count'] = round(group['LOAN COUNT'],0)
        drop_2 = ['ORIGINAL INTEREST RATE', 'BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL UPB', 'VINTAGE', 'LOAN COUNT',
                  'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                  'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        group1 = group.drop(drop_2, axis=1)
        return group1.sum()

    def avg_group(group):
        group['Avg UPB'] = round(group['ORIGINAL UPB'].mean(), 0)
        drop_2 = ['ORIGINAL INTEREST RATE', 'BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL UPB', 'VINTAGE', 'LOAN COUNT',
                  'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                  'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        group1 = group.drop(drop_2, axis=1)
        return group1.mean()

    def stats(group):
        return {'min': group.min(), 'max': group.max(), 'count': group.count(), 'mean': group.mean()}



#filtered on 100k records


def main():
    #get data
    a = GetData()
    acq_file_18Q1 = GetData.files_to_df(a, 'acq_files_analysis/acq_file_all.csv')
    #print(acq_file_18Q1.head()) #developer check
    #make basic transformations on the data
    b = DataTransformations()
    Vintage = DataTransformations.transformations(b, acq_file_18Q1)
    #print(Vintage.head()) #developer check
    #print(Vintage.sum().head()) #developer check
    #summarize data and return the groupby dataframe
    c = VintageSummary()
    byVintage = VintageSummary.call_summarization(c, Vintage)
    d = GetData.df_to_files(a, byVintage, 'acq_files_analysis/Acq_byVintage.csv')
    #print(byVintage)

if __name__ == "__main__":
    main()
