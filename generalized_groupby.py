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


        df = pd.read_csv(fname, sep = ",", usecols=filter_cols, nrows=filter_rows,)
        # print(df.head()) #developer check
        # print(df.shape) #develop check
        #print(df.columns)  #developer check
        #df1 = df.reset_index()
        drop = ['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0_x']
        df2 = df.drop(drop, axis=1)
        print(df2.head())
        print(df2.shape)
        return df2

    def df_to_files(self, df, fname):
        """
        Very generic write out to csv
        :param df_name:
        :param fname:
        :return:
        """
        df.to_csv(fname, sep=',')
        return


class GroupBySummary():

    def create_group_dict(self, by_field, wa_field, wa_list, sum_list, avg_list, report_name):
        """
        previous development, to create vintage dict
        by_field = 'UPB_BUCKET'
        wa_field = 'ORIGINAL UPB'
        wa_list = [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA', 'BORROWER CREDIT SCORE AT ORIGINATION'],
               ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'],
               ['LTV WA', 'ORIGINAL LOAN-TO-VALUE (LTV)'],
               ['CLTV WA', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA', 'ORIGINAL DEBT TO INCOME RATIO']]
        sum_list = [['Total_UPB', 'ORIGINAL UPB'], ['Total_Loan_Count', 'LOAN_COUNT']]
        avg_list = [['Avg UPB','ORIGINAL UPB']]
        :param by_field:
        :param wa_field:
        :param wa_list:
        :param sum_list:
        :param avg_list:
        :return:
        """
        dict = {}
        dict['by_field'] = by_field
        dict['wa_field'] = wa_field
        dict['wa_list'] = wa_list
        dict['sum_list'] = sum_list
        dict['avg_list'] = avg_list
        dict['report_name'] = report_name
        print(dict)
        return dict

    def generate_summmary(self, df, group_dict):
        x = CollectCompiledData()
        y = GroupBySummary()
        try:
            by_field = group_dict['by_field']
            wa_field = group_dict['wa_field']
            wa_list = group_dict['wa_list']
            sum_list = group_dict['sum_list']
            avg_list = group_dict['avg_list']
            report_name = group_dict['report_name']
        except ValueError:
            print("Error 1: Issue with Report Dictionary")
        else:
            b = GroupBySummary.sum_group(y, df, sum_list, by_field)
            c = GroupBySummary.avg_group(y, df, avg_list, by_field)
            d = GroupBySummary.wa_group(y, df, wa_list, wa_field, by_field)
            print(d.shape)
            print(d)
            e = pd.concat([b, c, d], axis=1)
            print(e.shape)
            print(e)
            fname = ('draft_groupby_data/'+report_name+'.csv')
            f = CollectCompiledData.df_to_files(x, e, fname)
            return e

    def wa_iterate(self, df, wa_list, weight, by_field):
        y = GroupBySummary()
        df1 = df
        # print("in wa_iterate",df1.head())
        dfs = []
        # wa_result = wa_list[0]
        # print("wa_results", wa_result)
        # df1[wa_result] = 0
        # wa_field = wa_list[1]
        # print("wa_field", wa_field)
        # df2 = GroupBySummary.wa_group(y, df1, wa_field, wa_result, weight, by_field)
        # dfs.append(df2)
        for l in wa_list:
            # print(l)
            wa_result = l[0]
            # print("wa_results",wa_result)
            df1[wa_result] = 0
            wa_field = l[1]
            # print("wa_field", wa_field)
            df2 = GroupBySummary.wa_group(y, df1, wa_field, wa_result, weight, by_field)
            dfs.append(df2)
        df3 = pd.concat(dfs, axis=1, ignore_index=False, sort=True)
        # print(df3)
        return df3


    def wa_group(self, df, wa_field, wa_result, weight, by_field):
        """
        original value for the weight_field was 'ORIGINAL UPB',
        the field by which the other fields are weighted for the average,
        in this case unpaid principal balance
        df['Int Rate WA'] = round((df['ORIGINAL INTEREST RATE'] * df[weight_field]).sum()/df[weight_field].sum(),1)
        original value for the drop fields:
        drop_2 = ['ORIGINAL INTEREST RATE','BORROWER CREDIT SCORE AT ORIGINATION','ORIGINAL UPB', 'VINTAGE','LOAN COUNT', 'CO-BORROWER CREDIT SCORE AT ORIGINATION', 'ORIGINAL LOAN-TO-VALUE (LTV)','ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO']
        removes all other fields subject to this wa_group calculation
        :param df:
        :param wa_field:
        :param wa_result:
        :param weight:
        :param by_field:
        :return:
        """
        cols = df.columns.tolist()
        # print(cols)
        cols.remove(by_field)
        cols.remove(wa_result)
        cols.remove(wa_field)
        cols.remove(weight)
        df1 = df.drop(cols, axis=1)  # get rid of all other columns you don't need, import for speed
        # print("in wa group", df1.head())
        df1[wa_result] = [(df1.loc[i, wa_field] * df1.loc[i, weight]) / df1.loc[i, weight] for i in range(len(df1[wa_field]))]
        # df1.loc[wa_result] = [(df1[i, wa_field] * df[weight]).sum() / df[weight].sum() for i in range(len(df1))]
        df2 = df1.drop(wa_field, axis=1)  # get rid of all other columns you don't need, import for speed
        df3 = df2.drop(weight, axis=1)
        df4 = df3.groupby(by_field)
        return df4.sum()

    def wa_iterate_loop(self, df, wa_list, weight, by_field):
        y = GroupBySummary()
        df1 = df
        # print("in wa_iterate",df1.head())
        dfs = []
        print(weight)
        print(by_field)
        # wa_result = wa_list[0]
        # print("wa_results", wa_result)
        # df1[wa_result] = 0
        # wa_field = wa_list[1]
        # print("wa_field", wa_field)
        # df2 = GroupBySummary.wa_group(y, df1, wa_field, wa_result, weight, by_field)
        # dfs.append(df2)
        for l in wa_list:
            print(l)
            wa_result = l[0]
            print("wa_results",wa_result)
            df1[wa_result] = 0
            wa_field = l[1]
            print("wa_field", wa_field)
            df2 = GroupBySummary.wa_group_loop(y, df1, wa_field, wa_result, weight, by_field)
            dfs.append(df2)
        df3 = pd.concat(dfs, axis=1, ignore_index=False, sort=True)
        # print(df3)
        return df3

    def wa_group_loop(self, df, wa_field, wa_result, weight, by_field):
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
        print(df.head())
        for i in range(len(df[wa_field])):
            # print(i)
            # print(df.loc[i, weight])
            df.loc[i, wa_result] = (df.loc[i, wa_field] * df.loc[i, weight]) / df.loc[i, weight]
        cols = df.columns.tolist()
        cols.remove(by_field)
        cols.remove(wa_result)
        # cols.remove(wa_field)
        # cols.remove(weight)
        df1 = df.drop(cols, axis=1)
        print(df1.columns)
        df2 = df1.groupby(by_field)
        print(df2)
        return df2.mean()

    def sum_group_loop(self, df, sum_list,by_field):
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

    def sum_iterate(self, df, sum_list, by_field):
        y = GroupBySummary()
        df1 = df
        dfs = []
        for l in sum_list:
            sum_result = l[0]
            df1[sum_result] = 0
            sum_field = l[1]
            df2 = GroupBySummary.sum_group(y, df1, sum_field, sum_result, by_field)
            dfs.append(df2)
        df3 = pd.concat(dfs, axis=1, ignore_index=False, sort=True)
        print(df3.head())
        return df3

    def sum_group(self, df, sum_field , sum_result, by_field):
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
        cols.remove(sum_result)
        cols.remove(sum_field)
        df1 = df.drop(cols, axis=1)  # get rid of all other columns you don't need, import for speed
        df1[sum_result] = (round(df1[sum_field], 0))
        df2 = df1.drop(sum_field, axis=1) #get rid of all other columns you don't need, import for speed
        df3 = df2.groupby(by_field)
        return df3.sum() #apply sum on the return

    def avg_iterate(self, df, avg_list, by_field):
        y = GroupBySummary()
        df1 = df
        dfs = []
        for l in avg_list:
            avg_result = l[0]
            df1[avg_result] = 0
            avg_field = l[1]
            df2 = GroupBySummary.avg_group(y, df1, avg_field, avg_result, by_field)
            dfs.append(df2)
        df3 = pd.concat(dfs, axis=1, ignore_index=False, sort=True)
        print(df3.head())
        return df3

    def avg_group(self, df, avg_field, avg_result, by_field):
        """

        :param df:
        :param avg_list:
        :param by_field:
        :return:
        """
        cols = df.columns.tolist()
        cols.remove(by_field)
        cols.remove(avg_result)
        cols.remove(avg_field)
        df1 = df.drop(cols, axis=1)  # get rid of all other columns you don't need, import for speed
        df1[avg_result] = (round(df1[avg_field], 0))
        df2 = df1.drop(avg_field, axis=1)  # get rid of all other columns you don't need, import for speed
        df3 = df2.groupby(by_field)
        return df3.mean()

    def avg_group_loop(self, df, avg_list, by_field):
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


    def stats(self, df, cols):
        df1 = df.drop(cols)
        dict = {'min': df1.min(), 'max': df1.max(), 'count': df1.count(), 'mean': df1.mean()}
        df2 = pd.DataFrame(dict)
        return df2


def main():
    x = CollectCompiledData()
    y = GroupBySummary()
    fname = 'draft_tagging_data/merge_data_tag_out_06-07.csv'
    filter_cols = None
    filter_rows = None
    a = CollectCompiledData.files_to_df(x, fname, filter_cols, filter_rows)
    # fname = ('draft_groupby_data/vintage_bucket_input.csv')
    # h = CollectCompiledData.df_to_files(y, a, fname)
    # print(a['ORIGINAL UPB'])
    # vintage_dict= {'by_field': 'UPB_BUCKET', 'wa_field': 'ORIGINAL UPB', 'wa_list': [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA', 'BORROWER CREDIT SCORE AT ORIGINATION'], ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'], ['LTV WA', 'ORIGINAL LOAN-TO-VALUE (LTV)'], ['CLTV WA', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA', 'ORIGINAL DEBT TO INCOME RATIO']], 'sum_list': [['Total_UPB', 'ORIGINAL UPB'], ['Total_Loan_Count', 'LOAN_COUNT']], 'avg_list': [['Avg UPB', 'ORIGINAL UPB']], 'report_name':'vintage_summary'}
    # b = GroupBySummary.generate_summmary(y, a, vintage_dict)
    sum_list = [['Total_UPB', 'ORIGINAL UPB'], ['Total_Loan_Count', 'LOAN_COUNT']]
    #TERM_BUCKET
    #VINTAGE
    #UPB_BUCKET
    #PROPERTY STATE
    #'MONTHLY REPORTING PERIOD'
    by_field = 'TERM_BUCKET'
    b = GroupBySummary.sum_iterate(y, a, sum_list, by_field)
    avg_list = [['Avg UPB', 'ORIGINAL UPB']]
    c = GroupBySummary.avg_iterate(y, a, avg_list, by_field)
    weight = 'ORIGINAL UPB'
    wa_list1 = ['Int Rate WA', 'ORIGINAL INTEREST RATE']
    wa_list = [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA', 'BORROWER CREDIT SCORE AT ORIGINATION'],
               ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'],
               ['LTV WA', 'ORIGINAL LOAN-TO-VALUE (LTV)'],
               ['CLTV WA', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA', 'ORIGINAL DEBT TO INCOME RATIO']]
    # d = GroupBySummary.wa_iterate(y, a, wa_list, weight, by_field)
    # print("from main\n", d)
    e = GroupBySummary.wa_iterate_loop(y, a, wa_list, weight, by_field)
    print('from main\n', e)
    # f = pd.concat([b, c, d], axis=1, ignore_index=False, sort=True)
    g = pd.concat([b, c, e], axis=1, ignore_index=False, sort=True)
    # fnamef = ('draft_groupby_data/vintage_bucket_lcmp.csv')
    fnameg = ('draft_groupby_data/term_bucket_06-07.csv')
    #'draft_groupby_data/reporting_period_bucket_06-07.csv'
    #'draft_groupby_data/term_bucket_06-07.csv'
    #draft_groupby_data/vintage_bucket_06-07.csv
    #draft_groupby_data/upb_bucket_06-07.csv
    # h = CollectCompiledData.df_to_files(y, f, fnamef)
    j = CollectCompiledData.df_to_files(y, g, fnameg)
    # fnamek = ('draft_groupby_data/vintage_bucket_results.csv')
    # k = CollectCompiledData.files_to_df(x, h)




if __name__ == '__main__':
    main()

# x = CollectCompiledData()
# filter_cols = None
# filter_rows = 15
# fname = 'draft_tagging_data/merge_data_tag_out.csv'
# a = CollectCompiledData.files_to_df(x, fname, filter_cols, filter_rows)
# print(a.head())
#
# y = GroupBySummary()
#
# by_field = 'UPB_BUCKET'
#
# weight = 'ORIGINAL UPB'
# wa_list = [['Int Rate WA', 'ORIGINAL INTEREST RATE'], ['BRW FICO WA', 'BORROWER CREDIT SCORE AT ORIGINATION'],
#                ['CO BRW FICO WA', 'CO-BORROWER CREDIT SCORE AT ORIGINATION'],
#                ['LTV WA', 'ORIGINAL LOAN-TO-VALUE (LTV)'],
#                ['CLTV WA', 'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)'], ['DTI WA', 'ORIGINAL DEBT TO INCOME RATIO']]
# wa_list1 = ['Int Rate WA', 'ORIGINAL INTEREST RATE']
# wa_result = 'Int Rate WA'
# wa_field = 'ORIGINAL INTEREST RATE'
# # for i in range(len(a[wa_field])):
# #     print(i)
# #     # a.loc[i,wa_result] = (a.loc[i, wa_field] * a.loc[i, weight]).sum() / a[weight].sum()
# #     a.loc[i, wa_result] = (a.loc[i, wa_field] * a.loc[i, weight]).sum() / a[weight].sum()
# #     print(a.loc[i, wa_result])
#
# a[wa_result] = [(a.loc[i, wa_field] * a.loc[i,weight]).sum() / a[weight].sum() for i in range(len(a[wa_field]))]
# print(a[wa_result])
# # df.loc[i, l[0]] = round((df.loc[i,l[1]] * df[weight_field]).sum() / df[weight_field].sum(), 0)