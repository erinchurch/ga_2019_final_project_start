import pandas as pd
import numpy as np

class GetData():

    def get_acq_loans(self, fname):
        acq_header_file = pd.read_csv('../Performance_All/some-acquisition/header_aquisition_file.txt', sep=",")
        # print("headers file", acq_header_file.head())

        columns = acq_header_file["Field Name"]
        # print("headers", columns)

        filter_columns = ['LOAN IDENTIFIER']
        # usecols=filter_columns
        # nrows=1000
        df = pd.read_csv(fname, sep="|", header=None, names=columns, nrows=100)

        return df

    def get_perf_loans(self,fname):
        df_columns = pd.read_csv('../Performance_All/some-performance/performance_file_headers.txt', sep=',')
        columns = df_columns['Field Name']
        # print(columns)
        # print(type(columns))
        headers = columns.tolist()
        # print(headers)

        filter_columns = ['LOAN IDENTIFIER']

        # usecols=filter_columns
        # nrows=1000
        df = pd.read_csv(fname, sep='|', header=None, names=headers, nrows=100)

        return df



def compare_acq_pop_loop(df1, field1, df2, field2):
    df1['PERF_FLAG'] = None
    df1.to_csv(('pre-' + 'PERF_FLAG' + '.csv'), sep=',')
    for i in df1[field1]:
        if df1.loc[i, field1] in df2[field2]:
            df1.loc[i,'PERF_FLAG'] = True
            #elif i != j:
                #df1.loc[i, 'PERF_FLAG'] = False
    df1.to_csv(('post-' + 'PERF_FLAG' + '.csv'), sep=',')
    df2.to_csv('other_data_set.csv', sep=',')
    print(df1.head())
    return df1

def compare_perf_pop_loop(df1, field1, df2, field2):
    #df2['ACQ_FLAG'] = False
    for i in df2[field2]:
        #print(i)
        for j in df1[field1]:
            #print(j)
            if i == j:
                df2.loc[i,'ACQ_FLAG'] = True
            #elif i != j:
                #df2.loc[i, 'ACQ_FLAG'] = False

    print(df2.head())
    return df2

def pop_compare_analysis(df, field):
    #print(df.head())
    df1 = df.groupby(field)
    print(df1.count())
    print(df1)
    return df1

def merge(df1, df2):
    df_new = pd.merge(df1, df2, on='LOAN IDENTIFIER', validate='m:1' )
    return df_new

def main():
    #get data
    y = GetData()
    acq_in_file = '../Performance_All/some-acquisition/Acquisition_2017Q2.txt'
    a = GetData.get_acq_loans(y, acq_in_file)
    source_acq = acq_in_file.replace('../Performance_All/some-acquisition/','')
    a['SOURCE_ACQ'] = source_acq
    print(a.head())
    print(a.shape)
    print(a.columns)
    perf_in_file = '../Performance_All/some-performance/Performance_2017Q2.txt'
    b = GetData.get_perf_loans(y, perf_in_file)
    source_perf = perf_in_file.replace('../Performance_All/some-performance/', '')
    b['SOURCE_PERF'] = source_perf
    print(b.shape)
    print(b.columns)
    a.to_csv('sample_acq_data.csv')
    b.to_csv('sample_perf_data.csv')
    print(b.head())
    c = merge(b, a)
    print(c.shape)
    print(c.columns)
    c.to_csv('sample_perf_acq_data.csv')


    #add population comparison flags
    #c = compare_acq_pop_loop(a,'LOAN IDENTIFIER', b,'LOAN IDENTIFIER')
    #d = compare_perf_pop_loop(a,'LOAN IDENTIFIER', b,'LOAN IDENTIFIER')
    #e = pop_compare_analysis(c, 'PERF_FLAG')
    #f = pop_compare_analysis(d, 'ACQ_FLAG')
    print('all done')

main()

"""
l1 = [100008626061, 100010363569, 100012442387, 100012535712, 100017029207]
l2 = [100008626061, 100008626061, 100008626061, 100010363569, 100010363569, 100010363569, 100012442387,100012442387,100012442387,]

test_s1 = pd.Series(l1)
print(test_s1)
test_s2 = pd.Series(l2)
print(test_s2)

for l in test_s1:
    #print('this is l in l1',l)
    for j in test_s2:
        #print('this j in l2', j)
        if l == j:
            print("this isl from s1,", l, "this is j from s2", j, "match", True)
        elif l !=j:
            print("this isl from s1,", l, "this is j from s2", j, "match", False)

dict1 = {'LOAN IDENTIFIER': test_s1}
dict2 = {'LOAN IDENTIFIER': test_s2}
test_df1 = pd.DataFrame(data=dict1)
#test_df1['PERF_MATCH'] = None
print(test_df1)
test_df2 = pd.DataFrame(data=dict2)
test_df2['PERF_MATCH2'] = 'PERF_FLAG'
print(test_df2)

field = ['LOAN IDENTIFIER']


test_df3 = test_df1.set_index('LOAN IDENTIFIER')
# # print(test_df3)
test_df4 = test_df2.set_index('LOAN IDENTIFIER')
s4 = test_df4['PERF_FLAG']
print(s4)
#print(test_df4)
# test_df5 = test_df3.merge(test_df4, how='left', left_index=True, right_index=True)
# print(test_df5)
# test_df5 = test_df3.merge(test_df2, how='inner', left_index=True, right_on='LOAN IDENTIFIER')
# print(test_df5)
test_df6 = pd.merge(test_df1, test_df2, how='left', on='LOAN IDENTIFIER', validate='1:m')
print(test_df6)
# test_df7 = test_df4.append(s4)
# print(test_df7)


"""

"""

for l in test_df1['LOAN IDENTIFER']:
    #print('this is l in df1', test_df1[l])
    print('this is L', l)
    #x = test_df1.loc[l]
    #print(x)
    for j in test_df2['LOAN IDENTIFIER']:
        #print('this j in l2', test_df2[j])
        print('this is l', l, 'this is J', j)
        #print(test_df1.loc[l])
        #y = test_df2.loc[j]
        #print(y)
        if l == j:
            print("this is l from df1,", l, "this is j from df2", j, "match", True)

 """



"""
when i get to enrichment of one file of the other
pandas.Series.where

"""