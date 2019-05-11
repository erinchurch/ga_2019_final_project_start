import pandas as pd
import numpy as np



def read_acq_files(fname):
    acq_header_file = pd.read_csv('some-acquisition/header_aquisition_file.txt', sep=",")
    # print("headers file", acq_header_file.head())

    columns = acq_header_file["Field Name"]
    # print("headers", columns)

    filter_columns = ['LOAN IDENTIFIER', 'ORIGINAL INTEREST RATE', 'ORIGINAL UPB',
                      'ORIGINATION DATE', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                      'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO',
                      'BORROWER CREDIT SCORE AT ORIGINATION', 'CO-BORROWER CREDIT SCORE AT ORIGINATION']
    #usecols=filter_columns
    #nrows=1000
    df = pd.read_csv(fname, sep="|", header=None, names=columns, infer_datetime_format=True, nrows=1000)
    print(df.shape)
    print(df.columns)
    print(df['BORROWER CREDIT SCORE AT ORIGINATION'].max())
    print(df['BORROWER CREDIT SCORE AT ORIGINATION'].min())
    print(df['PRODUCT TYPE'].head())
    print(df.loc[416, 'BORROWER CREDIT SCORE AT ORIGINATION'])
    df['BORROWER CREDIT SCORE AT ORIGINATION'].to_csv('some-acquisition/validate_FICO.csv', sep=',')

    return df


def make_test_df():
    test_s = pd.Series([450.0, 390.0, 560.0, 680.0, 790.0, 890.0, 450.0, 823.0])  # test series
    dict = {'VALUES': test_s, }
    test_df = pd.DataFrame(data=dict)
    test_df['BUCKET'] = None
    print('set up df in the make test df function\n', test_df)
    return test_df


def set_bucket():
    bucket_base = np.arange(300.0, 900.0, 50.0)  # generate the buckets
    # list compression style
    # bucket_base = [0,10,20,30,40,50,60,70,80,90,100,120,130,140,150,160]
    print("bucket base in teh set buckets function\n", bucket_base)
    buckets = [[x, x + 50.0] for x in bucket_base if x <= 900.0]  # generate the bucket range - WORKS
    print("buckets in the set function\n", buckets)
    return buckets


def set_buckets_given_params(min, max, incr):
    bucket_base = np.arange(min, max, incr)  # generate the buckets
    # list compression style
    # bucket_base = [0,10,20,30,40,50,60,70,80,90,100,120,130,140,150,160]
    print("bucket base in set bucket given parameters fucntion\n", bucket_base)
    buckets = [[x, x + incr] for x in bucket_base if x <= max]  # generate the bucket range - WORKS
    print("buckets in the set buckets given parameters\n", buckets)
    return buckets

def use_bucket_for_given_df(df, buckets):
    test_df = df
    print('df provided to use bucket for given df\n', test_df)
    # apply to df with for loop
    for i in range(len(test_df['VALUES'])):
        print(test_df.loc[i, 'VALUES'])
        print(test_df.loc[i, 'BUCKET'])
        for b in buckets:
            # print(l2)
            if b[0] <= test_df.loc[i, 'VALUES'] and test_df.loc[i, 'VALUES'] < b[1]:
                test_df.loc[i, 'BUCKET'] = b[1]
    print('modified df in the us bucket loop given df\n', test_df.head())
    return test_df

def use_bucket_for_g_df_g_flds(df, buckets, x, y):
    test_df = df
    test_df[y] = None
    print('df provided into use bucket for given df\n', test_df.head())
    # apply to df with for loop
    for i in range(len(test_df[x])):
        #print(test_df.loc[i, x])
        #print(test_df.loc[i, y])
        for b in buckets:
            # print(l2)
            if b[0] <= test_df.loc[i, x] and test_df.loc[i, x] < b[1]:
                test_df.loc[i, y] = b[1]
    print('modified df results in the us bucket loop given df and given df fields\n', test_df.head())
    return test_df

def use_bucket_for(buckets):
    test_s = pd.Series([450.0, 390.0, 560.0, 680.0, 790.0, 890.0, 450.0, 823.0])  # test series
    dict = {'VALUES': test_s, }
    test_df = pd.DataFrame(data=dict)
    test_df['BUCKET'] = None
    print('set up df in the use bucket for function\n', test_df)
    # apply to df with for loop
    for i in range(len(test_df['VALUES'])):
        print(test_df.loc[i, 'VALUES'])
        print(test_df.loc[i, 'BUCKET'])
        for b in buckets:
            # print(l2)
            if b[0] <= test_df.loc[i, 'VALUES'] and test_df.loc[i, 'VALUES'] < b[1]:
                test_df.loc[i, 'BUCKET'] = b[1]
    print('modified df in the use bucket for loop\n', test_df)
    return test_df

def use_bucket_list_compr(buckets):
    test_s = pd.Series([450.0, 390.0, 560.0, 680.0, 790.0, 890.0, 450.0, 823.0])  # test series
    dict = {'VALUES': test_s, }
    test_df2 = pd.DataFrame(data=dict)
    test_df2['BUCKET'] = None
    print('set up df2 in the use bucket for function\n', test_df2)
    # list comprehension style
    test_df2['BUCKET'] = [b[1] for i in range(len(test_df2)) for b in buckets if b[0] <= test_df2.loc[i, 'VALUES'] and test_df2.loc[i, 'VALUES'] < b[1]]
    print('modified df2 in the use buck list comprehension function\n', test_df2)
    return test_df2


def use_bucket_list_compr_given_df(df, buckets):
    test_df2 = df
    print('df provided to use buckets list compr given df\n', test_df2)
    # list comprehension style
    test_df2['BUCKET'] = [b[1] for i in range(len(test_df2)) for b in buckets if b[0] <= test_df2.loc[i, 'VALUES'] and test_df2.loc[i, 'VALUES'] < b[1]]
    print('modified df2 in the use buck list comprehension function given df\n', test_df2.head())
    return test_df2


def use_bucket_list_compr_given_df_v2(df, buckets):
    print('df provided to use buckets list compr given df\n', df)
    # list comprehension style
    df['BUCKET'] = [b[1] for i in range(len(df)) for b in buckets if b[0] <= df.loc[i, 'VALUES'] and df.loc[i, 'VALUES'] < b[1]]
    print('modified df2 in the use buck list comprehension function given df version 2\n', df.head())
    return df

def use_bucket_list_compr_g_df_g_bkt_g_fld(df, buckets, x, y,z):
    print('df provided into use buckets list compr given df given fields\n', df.head())
    df[x].fillna(value=z, inplace=True)
    print(z)
    print(df.loc[416,x])
    df[y] = None
    # list comprehension style
    df[y] = [b[1] for i in range(len(df)) for b in buckets if b[0] <= df.loc[i, x] and df.loc[i, x] < b[1]]
    print('modified df2 resulting buck list comprehension function given df and given df fields\n', df.head())
    return df

def use_bucket_list_compr_g_df_g_bkt_g_fld_v2(df, buckets, x, y, z):
    print('df provided into use buckets list compr given df given fields\n', df.head())
    df[x] = df[x].replace(to_replace='nan', value = z, inplace=True)
    df[y] = None
    print('df provided into use buckets list compr given df given fields\n', df.head())
    # list comprehension style
    df[y] = [b[1] for i in range(len(df))(print(df.loc[i, x]))(print(df.loc[i, y])) for b in buckets if b[0] <= df.loc[i, x] and df.loc[i, x] < b[1]]
    print('modified df2 resulting buck list comprehension function given df and given df fields\n', df.head())
    return df

def orig():

    bucket_base = np.arange(300.0, 900.0, 50.0) #generate the buckets

    #list compression style
    # bucket_base = [0,10,20,30,40,50,60,70,80,90,100,120,130,140,150,160]
    print("bucket base in the original function\n",bucket_base)
    buckets = [[x, x+50.0] for x in bucket_base if x <= 900.0] #generate the bucket range - WORKS
    print("buckets in the original function\n",buckets)

    test_s = pd.Series([450.0,390.0,560.0,680.0,790.0,890.0,450.0,823.0]) #test series
    dict = {'VALUES':test_s,}
    test_df = pd.DataFrame(data=dict)
    test_df['BUCKET'] = None
    print('set up df', test_df)
    test_df2 = pd.DataFrame(data=dict)
    test_df2['BUCKET'] = None
    print('set up df2 in the original function \n', test_df2)
    #apply to df with for loop
    for i in range(len(test_df['VALUES'])):
        print(test_df.loc[i, 'VALUES'])
        print(test_df.loc[i, 'BUCKET'])
        for l2 in buckets:
            #print(l2)
            if l2[0] <= test_df.loc[i, 'VALUES'] and test_df.loc[i, 'VALUES'] < l2[1]:
                test_df.loc[i, 'BUCKET'] = l2[1]
    print('modified df in teh original function\n',test_df)
    #list comprehension style
    test_df2['BUCKET'] = [l2[1] for i in range(len(test_df2)) for l2 in buckets if l2[0] <= test_df2.loc[i, 'VALUES'] and test_df2.loc[i, 'VALUES'] < l2[1]]
    print('modified df2 in the original function\n', test_df2)
    return test_df2


def main():
    #original set of tests that were global adn work in main
    #df_orig = orig()
    # buckets = set_bucket()
    # df_loop = use_bucket_for(buckets)
    # df_list = use_bucket_list_compr(buckets)
    # df_test = make_test_df()
    # df_loop_given_df = use_bucket_for_given_df(df_test, buckets)
    # df_list_given_df = use_bucket_list_compr_given_df(df_test, buckets)
    # df_list_given_df_v2 = use_bucket_list_compr_given_df_v2(df_test, buckets)

    #second set of test that were global and work in main
    min = 300.0
    max = 900.0
    incr = 50.0

    buckets_g_params = set_buckets_given_params(min, max, incr)
    df_loop_b2 = use_bucket_for(buckets_g_params)
    df_list_b2 = use_bucket_list_compr(buckets_g_params)
    df_test_b2 = make_test_df()
    df_loop_given_df_b2 = use_bucket_for_given_df(df_test_b2, buckets_g_params)
    df_list_given_df_b2 = use_bucket_list_compr_given_df(df_test_b2, buckets_g_params)
    df_list_given_df_v2_b2 = use_bucket_list_compr_given_df_v2(df_test_b2, buckets_g_params)


    # third set of tests done from MAIN
    # min = 300.0
    # max = 900.0
    # incr = 50.0
    #
    # df_values = 'VALUES'
    # df_tag = 'BUCKET'
    #
    # buckets_g_params = set_buckets_given_params(min, max, incr)
    # # df_loop_b2 = use_bucket_for_(buckets_g_params) #depricate test
    # # df_list_b2 = use_bucket_list_compr(buckets_g_params) #depreicate test
    # df_test_b2 = make_test_df()
    # df_loop_given_df_b2 = use_bucket_for_g_df_g_flds(df_test_b2, buckets_g_params, df_values, df_tag)
    # df_list_given_df_b2 = use_bucket_list_compr_g_df_g_bkt_g_fld(df_test_b2, buckets_g_params, df_values, df_tag)





#main()


#original set of tests done from global
#df_orig = orig()
# buckets = set_bucket()
# df_loop = use_bucket_for(buckets)
# df_list = use_bucket_list_compr(buckets)
# df_test = make_test_df()
# df_loop_given_df = use_bucket_for_given_df(df_test, buckets)
# df_list_given_df = use_bucket_list_compr_given_df(df_test, buckets)
# df_list_given_df_v2 = use_bucket_list_compr_given_df_v2(df_test, buckets)

#second set of tests done from global
# min = 300.0
# max = 900.0
# incr = 50.0
#
# buckets_g_params = set_buckets_given_params(min, max, incr)
# df_loop_b2 = use_bucket_for(buckets_g_params)
# df_list_b2 = use_bucket_list_compr(buckets_g_params)
# df_test_b2 = make_test_df()
# df_loop_given_df_b2 = use_bucket_for_given_df(df_test_b2, buckets_g_params)
# df_list_given_df_b2 = use_bucket_list_compr_given_df(df_test_b2, buckets_g_params)
# df_list_given_df_v2_b2 = use_bucket_list_compr_given_df_v2(df_test_b2, buckets_g_params)

# #third set of tests done from global
# min = 300.0
# max = 900.0
# incr = 50.0
#
# df_values = 'VALUES'
# df_tag = 'BUCKET'
#
# buckets_g_params = set_buckets_given_params(min, max, incr)
# # df_loop_b2 = use_bucket_for_(buckets_g_params)
# # df_list_b2 = use_bucket_list_compr(buckets_g_params)
# df_test_b2 = make_test_df()
# df_loop_given_df_b2 = use_bucket_for_g_df_g_flds(df_test_b2, buckets_g_params, df_values, df_tag)
# df_list_given_df_b2 = use_bucket_list_compr_g_df_g_bkt_g_fld(df_test_b2, buckets_g_params, df_values, df_tag)
#


#forth set of tests done from global
print('4th test')
file = 'some-acquisition/Acquisition_2017Q2.txt'
acq_df = read_acq_files(file)
print(acq_df.head())
min = 300.0
max = 900.0
incr = 50.0
sub = 700.0
df_values = 'BORROWER CREDIT SCORE AT ORIGINATION'
df_tag = 'FICO_BUCKET'

buckets_g_params = set_buckets_given_params(min, max, incr)
#df_loop_b2 = use_bucket_for(buckets_g_params) #decom, have pre-made df
#df_list_b2 = use_bucket_list_compr(buckets_g_params) #decome, have pre-made df
#df_test_b2 = make_test_df() #decome, have pre-made df
df_loop_given_real_df_b2 = use_bucket_for_g_df_g_flds(acq_df, buckets_g_params, df_values, df_tag)
df_list_given_real_df_b2 = use_bucket_list_compr_g_df_g_bkt_g_fld(acq_df, buckets_g_params, df_values, df_tag, sub)
#df_list_given_real_df_b2_v2 = use_bucket_list_compr_g_df_g_bkt_g_fld_v2(acq_df, buckets_g_params, df_values, df_tag, sub)

