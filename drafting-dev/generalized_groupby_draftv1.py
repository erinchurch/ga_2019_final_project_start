#taken from previously created home work submission
#originally based on Vintage

#generalize to be able to group by any feature, vintage yr, month, product type, upb or term group

import pandas as pd

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


class CollectCompiledData():

    def __init__(self):
        #NOTE OF EXISTING COMMON REPORT BUCKETS FROM THE VINTAGE ACQ REPORTS
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


    def files_to_df(self, fname, filter_cols, filter_rows):
        """
        Collect merge file data, although the pd.read_csv() is general enough to be able to support
        any comma separate data.

        Not currently column or row filtered but could add filter of column data to improve performance

        Index also not currently overwritten, but could be done.

        unused arguments:

        # index = 'LOAN IDENTIFIER'
        # index_col = index
        #index_col=False,
        #usecols=filter_columns,
        #nrows = 1000

        """
        known_columns = ['LOAN IDENTIFIER', 'MONTHLY REPORTING PERIOD', 'SERVICER NAME',
                         'CURRENT INTEREST RATE', 'CURRENT ACTUAL UPB', 'LOAN AGE',
                         'REMAINING MONTHS TO LEGAL MATURITY', 'ADJUSTED MONTHS TO MATURITY',
                         'MATURITY DATE', 'METROPOLITAN STATISTICAL AREA (MSA)',
                         'CURRENT LOAN DELINQUENCY STATUS', 'MODIFICATION FLAG',
                         'ZERO BALANCE CODE', 'ZERO BALANCE EFFECTIVE DATE',
                         'LAST PAID INSTALLMENT DATE', 'FORECLOSURE DATE', 'DISPOSITION DATE',
                         'FORECLOSURE COSTS', 'PROPERTY PRESERVATION AND REPAIR COSTS',
                         'ASSET RECOVERY COSTS', 'MISCELLANEOUS HOLDING EXPENSES AND CREDITS',
                         'ASSOCIATED TAXES FOR HOLDING PROPERTY', 'NET SALE PROCEEDS',
                         'CREDIT ENHANCEMENT PROCEEDS', 'REPURCHASE MAKE WHOLE PROCEEDS',
                         'OTHER FORECLOSURE PROCEEDS', 'NON INTEREST BEARING UPB',
                         'PRINCIPALFORGIVENESS AMOUNT', 'REPURCHASE MAKE WHOLE PROCEEDS FLAG',
                         'FORECLOSURE PRINCIPAL WRITE-OFF AMOUNT',
                         'SERVICING ACTIVITY INDICATOR', 'SOURCE_x', 'ORIGINATION CHANNEL',
                         'SELLER NAME', 'ORIGINAL INTEREST RATE', 'ORIGINAL UPB',
                         'ORIGINAL LOAN TERM', 'ORIGINATION DATE', 'FIRST PAYMENT DATE',
                         'ORIGINAL LOAN-TO-VALUE (LTV)',
                         'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'NUMBER OF BORROWERS',
                         'ORIGINAL DEBT TO INCOME RATIO', 'BORROWER CREDIT SCORE AT ORIGINATION',
                         'FIRST TIME HOME BUYER INDICATOR', 'LOAN PURPOSE', 'PROPERTY TYPE',
                         'NUMBER OF UNITS', 'OCCUPANCY TYPE', 'PROPERTY STATE', 'ZIP CODE SHORT',
                         'PRIMARY MORTGAGE INSURANCE PERCENT', 'PRODUCT TYPE',
                         'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'MORTGAGE INSURANCE TYPE',
                         'RELOCATION MORTGAGE INDICATOR', 'SOURCE_y'] #just an FYI for this specific merged file


        df = pd.read_csv(fname, sep = ",", usecols=filter_cols, nrows=filter_rows)
        print(df.head()) #developer check
        print(df.shape) #develop check
        #print(df.columns)  #developer check
        return df


    def df_to_files(self, df_name, fname):
        """
        Very generic write out to csv
        :param df_name:
        :param fname:
        :return:
        """
        df_name.to_csv(fname, sep=',')
        return



class GroupBySummary():

    def call_summarization(self, df, by_field):
        pass


    def wa_group(self, df, wa_list, weight_field, by_field):
        """
        original value for the weight_field was 'ORIGINAL UPB',
        the field by which the other fields are weighted for the average,
        in this case unpaid principal balance
        df['Int Rate WA'] = round((df['ORIGINAL INTEREST RATE'] * df[weight_field]).sum()/df[weight_field].sum(),1)
        original value for the drop fields:
        drop_2 = ['ORIGINAL INTEREST RATE','BORROWER CREDIT SCORE AT ORIGINATION','ORIGINAL UPB', 'VINTAGE','LOAN COUNT', 'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)','ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        removes all other fields subject to this wa_group calculation
        :param df:
        :param weight_field:
        :param wa_list:
        :param by_field:
        :return:
        """
        cols = df.columns.tolist()
        cols.remove(by_field)
        for l in wa_list:
            for i in range(len(df)):
                #print(l)
                df.loc[i, l[0]] = round((df.loc[i,l[1]] * df[weight_field]).sum() / df[weight_field].sum(), 0)
        df1 = df.drop(cols, axis=1)
        df2 = df1.groupby(by_field)
        return df2.mean()

    def sum_group(self, df, sum_list,by_field):
        """
        df['Total UPB'] = round(df['ORIGINAL UPB'],0)
        df['Loan Count'] = round(df['LOAN COUNT'],0)
        drop_2 = ['ORIGINAL INTEREST RATE', 'BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL UPB', 'VINTAGE', 'LOAN COUNT',
                  'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                  'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        :param df:
        :param sum_list:
        :param by_field:
        :return:
        """
        cols = df.columns.tolist()
        cols.remove(by_field)
        for l in sum_list: #for the fields in the sum_list
            #print(l)
            df[l[0]] = round(df[l[1]], 0)  #copy them to the new field, round them
        df1 = df.drop(cols, axis=1) #get rid of all other columns you don't need, import for speed
        df2 = df1.groupby(by_field)
        return df2.sum() #apply sum on the return


    def avg_group(self, df, avg_list, by_field):
        """

        :param df:
        :param avg_list:
        :param by_field:
        :return:
        """
        cols = df.columns.tolist()  # collect all the columns in the data set
        cols.remove(by_field)
        for list in avg_list: #for the fields in the sum_list
            df[list[0]] = round(df[list[1]].mean(), 0)  #copy them to the new field, round them
        df1 = df.drop(cols, axis=1) #get rid of all other columns you don't need, import for speed
        df2 = df1.groupby(by_field)
        return df2.mean()

    def stats(self, df):
        return {'min': df.min(), 'max': df.max(), 'count': df.count(), 'mean': df.mean()}


def main():
    #works
    x = CollectCompiledData()
    y = GroupBySummary()
    fname = '../draft_tagging_data/merge_data_tag_out.csv'
    filter_cols = None
    filter_rows = 10000
    a = CollectCompiledData.files_to_df(x, fname, filter_cols, filter_rows)

    by_field = 'UPB_BUCKET'
    wa_field = 'ORIGINAL UPB'
    wa_list = [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA', 'BORROWER CREDIT SCORE AT ORIGINATION'],
               ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'],
               ['LTV WA', 'ORIGINAL LOAN-TO-VALUE (LTV)'],
               ['CLTV WA', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA', 'ORIGINAL DEBT TO INCOME RATIO']]
    sum_list = [['Total_UPB', 'ORIGINAL UPB'], ['Total_Loan_Count', 'LOAN_COUNT']]
    avg_list = [['Avg UPB','ORIGINAL UPB']]

    b = GroupBySummary.sum_group(y, a, sum_list, by_field)
    c = GroupBySummary.avg_group(y, a, avg_list, by_field)
    d = GroupBySummary.wa_group(y, a, wa_list, wa_field, by_field)
    print(d.shape)
    print(d)
    e = pd.concat([b, c, d], axis=1)
    print(e.shape)
    print(e)

if __name__ == '__main__':
    main()



"""
            Total_UPB  Total_Loan_Count   ...    CLTV WA  DTI WA
UPB_BUCKET                                ...                   
0             6012000               148   ...       72.9    33.2
50000        63307000               792   ...       72.9    33.2
100000      180488000              1436   ...       72.9    33.2
150000      340235000              1959   ...       72.9    33.2
200000      301378000              1359   ...       72.9    33.2
250000      365546000              1359   ...       72.9    33.2
300000      343743000              1069   ...       72.9    33.2
350000      356070000               966   ...       72.9    33.2
400000      180082000               432   ...       72.9    33.2
450000       60670000               131   ...       72.9    33.2
500000       91306000               177   ...       72.9    33.2
550000       44680000                78   ...       72.9    33.2
600000       58101000                94   ...       72.9    33.2

[13 rows x 9 columns]

Process finished with exit code 0
"""


# wa_field = ['ORIGINAL UPB']
#
# filter = None
#
# df = pd.read_csv('../draft_groupby_data/dev_groupby_sample.csv', sep = ",", usecols= filter)
#
#
# wa_list = [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA','BORROWER CREDIT SCORE AT ORIGINATION'],
#                    ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'], ['LTV WA','ORIGINAL LOAN-TO-VALUE (LTV)'],
#                    ['CLTV WA','ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA','ORIGINAL DEBT TO INCOME RATIO']]
#
# sum_list = [['Total_UPB','ORIGINAL UPB'],['Total_Loan_Count','LOAN_COUNT']]



#df['Int Rate WA'] = round((df['ORIGINAL INTEREST RATE'] * df[weight_field]).sum() / df[weight_field].sum(), 1)
# weight_field = 'ORIGINAL UPB'
# orig_cols = df.columns.tolist()
# orig_cols.remove('UPB_BUCKET')
# print(orig_cols)
# print(df['ORIGINAL INTEREST RATE'].head())
# print(df['ORIGINAL INTEREST RATE'].tail())
# for list in wa_list:
#     df[list[0]] = round((df[list[1]]*df[weight_field]).sum()/df[weight_field].sum(), 1)
# mid_columns = df.columns.tolist()
# print(mid_columns)
# df1 = df.drop(orig_cols, axis=1)
# print(df1.head())
# print(df1.groupby(['UPB_BUCKET']).mean())


# #works SUM LOOP
# orig_cols = df.columns.tolist()
# orig_cols.remove('UPB_BUCKET')
# print(orig_cols)
# for list in sum_list:
#     df[list[0]] = round(df[list[1]], 0)
#     mid_columns = df.columns.tolist()
#     print(mid_columns)
#     df1 = df.drop(orig_cols, axis=1)
#     print(df1.groupby(['UPB_BUCKET']).sum())

# # sum list compr DOESNT WORK
# orig_cols = df.columns.tolist()
# orig_cols.remove('UPB_BUCKET')
# print(orig_cols)
# df[list[0]] = [[df[list[1]]] for list in sum_list]
# mid_columns = df.columns.tolist()
# print(mid_columns)
# df1 = df.drop(orig_cols, axis=1)
# print(df1.groupby(['UPB_BUCKET']).sum())
