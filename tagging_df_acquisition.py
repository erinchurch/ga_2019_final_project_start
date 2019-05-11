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
    return df


def bucket_for_loop(list_name, min, max, increment):
    # much slower
    base_list = np.arange(min, max, increment) #generate the bucket levels
    for x in base_list: #for bucket level in base list
        if x <= max: #if the bucket level is between in the min and max
            list_name += [[x, x+increment]]  #create the bounds the bucket
    return list_name  #give back the list containing bucket bounds

def bucket_list(list_name, min, max, increment):  #same as bucket() but in list comprehension form
    base_list = np.arange(min, max, increment)  #generate the bucket levels
    list_name = [[x, x + increment] for x in base_list if x <= max]
    return list_name

def bucket_list2(list_name, min, max, increment):
    base_list = np.arange(min, max, increment)
    print(base_list)
    list_name = [[x, x+increment] for x in base_list if x <= max] #generate the bucket range - WORKS
    print('list in bucket func', list_name)
    return list_name

def df_bucket_for_loop(df, df_field, df_bucket_name, bucket_list):  #same as df_bucket_list_comp but in for loop form
    #much slower
    #not an integer centric function
    df[df_bucket_name] = None #create the new bucket key field
    print('check iterable length',len(df[df_field]))
    print('check iterable length range', df.size)
    for i in range(len(df[df_field])):  #for value in df series
        #print(df.loc[i, df_field]) #developer check to print the value in the df series
        #print(df.loc[i, df_bucket_name]) #developer check to print the destination bucket value, should be None
        for b in bucket_list:  #for the bucket min, max in the bucket list provided
            # print(b) #developer check
            if b[0] <= df.loc[i, df_field] and df.loc[i, df_field] < b[1]:  #if the value in the df series is between the bucket list min, max
                df.loc[i, df_bucket_name] = b[1]  #update the df bucket name value to be the value of the bucket max
    print('modified df', df.head()) #developer check
    return df  #return the dataframe after update

def df_bucket(df, df_field, df_bucket_name, bucket_list):  #same as df_bucket but in list comprehension form
    #data type of df series and buckets should match
    print('check iterable length', len(df[df_field]))
    print('check iterable length range', df.size)
    df[df_bucket_name] = [b[1] for i in range(len(df)) for b in bucket_list if b[0] <= df.loc[i, df_field] and df.loc[i, df_field] < b[1]]
    #test_df2['BUCKET'] = [l2[1] for i in range(len(test_df2)) for l2 in buckets if l2[0] <= test_df2.loc[i, 'VALUES'] and test_df2.loc[i, 'VALUES'] < l2[1]]

    print('modified df2 in df_bucket for loop function\n', df.head())  #developer check
    return df #return the dataframe after update

def df_bucket2(df, x, y, list):
    # data type of df series and buckets should match
    df[y] = [l[1] for i in range(len(df)) for l in list if l[0] <= df.loc[i, x] and df.loc[i, x] < l[1]]
    print('modified df2 in df_bucket2 function\n', df.head())
    return df #return the dataframe after update

def nan_fix(df, df_field, enrich):
    df[df_field].fillna(value=enrich, inplace=True)
    return df  # return the dataframe after update

def count_loop(df, x, y): #for loop style
    for i in df[x]:
        if i != 'NaN' or i != 0:
            df[y] = 1
        else:
            df[y] = 0
    return df

def count(df, x, y): #list compression style
    df[y] = [1 for i in df[x] if i != 'NaN' or i != 0]
    return df

def vintage_yr(df, x, y):
    df[y] = pd.DatetimeIndex(df[x]).year
    return df

def vintage_mnth(df, x, y):
    df[y] = pd.DatetimeIndex(df[x]).month
    return df

def main():
    #get data WORKS
    file = 'some-acquisition/Acquisition_2017Q2.txt'
    acq_df = read_acq_files(file)
    print(acq_df.head())

    #loan count - WORKS
    # loan_num = 'LOAN IDENTIFIER'
    # loan_count = 'LOAN_COUNT'
    # #acq_df_ln_ct = count_loop(acq_df, loan_num, loan_count)
    # acq_df_ln_ct = count(acq_df, loan_num, loan_count)
    # print(acq_df_ln_ct.head())

    #vintage - WORKS
    # orig_dt = 'ORIGINATION DATE'
    # vintage_y = 'VINTAGE_YEAR'
    # vintage_m = 'VINTAGE_MONTH'
    # acq_df_vintage = vintage_yr(acq_df_ln_ct, orig_dt, vintage_y)
    # print(acq_df_vintage.head())
    # acq_df_vintage = vintage_mnth(acq_df_ln_ct, orig_dt, vintage_m)
    # print(acq_df_vintage.head())

    #create buckets WORKS
    #LTV bucket
    # ltv_min = 0
    # ltv_max = 200
    # ltv_incr = 10
    # ltv_bucket = []
    # ltv_bucket = bucket_list(ltv_bucket, ltv_min, ltv_max, ltv_incr)

    #UPB bucket
    upb_min = 0
    upb_max = 2000000
    upb_incr = 50000
    upb_bucket = []
    upb_bucket = bucket_list(upb_bucket, upb_min, upb_max, upb_incr)

    #FICO bucket
    #data type of bucket has to match data type it is being applied to
    fico_min = 300.0
    fico_max = 900.0
    fico_incr = 50.0
    fico_bucket = []
    #test
    fico_bucket = bucket_list2(fico_bucket, fico_min, fico_max, fico_incr)
    #works
    #fico_bucket = bucket_list(fico_bucket, fico_min, fico_max, fico_incr)
    print(fico_bucket)

    #apply buckets WORKS
    #LTV bucket WORKS
    # s_LTV = 'ORIGINAL LOAN-TO-VALUE (LTV)'
    # b_LTV = 'LTV_BUCKET'
    # acq_df_LTV = df_bucket(acq_df, s_LTV, b_LTV, ltv_bucket)
    # print('apply ltv bucket in main')
    # print(acq_df_LTV.head())

    #UPB bucket WORKS
    s_UPB = 'ORIGINAL UPB'
    b_UPB = 'UPB_BUCKET'
    acq_df_UPB = df_bucket(acq_df, s_UPB, b_UPB, upb_bucket)
    print('apply upb bucket via list compre in main')
    print(acq_df_UPB.head())
    acq_df_UPB2 = df_bucket_for_loop(acq_df, s_UPB, b_UPB, upb_bucket)
    print('apply upb bucket via for loop in main')
    print(acq_df_UPB2.head())

    # FICO bucket PARTIALLY DOESN'T WORK
    # FICO bucket PART WORKS
    s_FICO = 'BORROWER CREDIT SCORE AT ORIGINATION'
    enrich_FICO_nan = 700.0
    acq_df_fico_prep = nan_fix(acq_df, s_FICO, enrich_FICO_nan)
    # FICO bucket PART WORKS
    b_FICO = 'FICO_BUCKET'
    acq_df_FICO = df_bucket_for_loop(acq_df_fico_prep, s_FICO, b_FICO, fico_bucket)
    print('apply fico  via for loop bucket in main')
    print(acq_df_FICO.head())

    # FICO bucket PART DOESN'T WORK
    acq_df_FICO2 = df_bucket2(acq_df_fico_prep, s_FICO, b_FICO, fico_bucket)
    print('apply fico bucket 2 in main')
    print(acq_df_FICO2.head())

    # print(acq_df['BORROWER CREDIT SCORE AT ORIGINATION'].dtypes)
    # print(acq_df['ORIGINAL UPB'].dtypes)


main()



# bucket_base = np.arange(300.0, 900.0, 50.0) #generate the buckets
#
# #list compression style
# # bucket_base = [0,10,20,30,40,50,60,70,80,90,100,120,130,140,150,160]
# print("bucket base",bucket_base)
# buckets = [[x, x+50.0] for x in bucket_base if x <= 900.0] #generate the bucket range - WORKS
# print("buckets",buckets)
#
# test_s = pd.Series([450.0,390.0,560.0,680.0,790.0,890.0,450.0,823.0]) #test series
# dict = {'VALUES':test_s,}
# test_df = pd.DataFrame(data=dict)
# test_df['BUCKET'] = None
# print('set up df', test_df)
# test_df2 = pd.DataFrame(data=dict)
# test_df2['BUCKET'] = None
# print('set up df2', test_df2)
# #apply to df with for loop
# for i in range(len(test_df['VALUES'])):
#     print(test_df.loc[i, 'VALUES'])
#     print(test_df.loc[i, 'BUCKET'])
#     for l2 in buckets:
#         #print(l2)
#         if l2[0] <= test_df.loc[i, 'VALUES'] and test_df.loc[i, 'VALUES'] < l2[1]:
#             test_df.loc[i, 'BUCKET'] = l2[1]
# print('modified df',test_df)
# #list comprehension style
# test_df2['BUCKET'] = [l2[1] for i in range(len(test_df2)) for l2 in buckets if l2[0] <= test_df2.loc[i, 'VALUES'] and test_df2.loc[i, 'VALUES'] < l2[1]]
# print('modified df2', test_df2)

"""

#BUCKET CREATION

bucket_min = 0 #when create the buckets function, add these
bucket_max = 160 #when create the buckets function, add these
bucket_increment = 10 #when create the buckets function, add these

bucket_base = np.arange(0, 160, 10) #generate the buckets

#list compression style
# bucket_base = [0,10,20,30,40,50,60,70,80,90,100,120,130,140,150,160]
print("bucket base",bucket_base)
buckets = [[x, x+10] for x in bucket_base if x <= 200] #generate the bucket range - WORKS
print("buckets",buckets)

#full for loop style - WORKS
buckets_2 = []
for x in bucket_base:
    if x >= 0 or x <=200:
        buckets_2 += [[x, x+10]]
print("buckets 2",buckets_2)

"""



"""
learning to apply buckets and look up in lists, series and dataframes

#for item in list, series or a df, what is the value of item[0], item [1]
#if you have the base buckets, if series value is between x and x+10, return value


#for item in list, what is the value of item[0], item [1]
#apply bucket to a list
list = [1,2,3,4,66,7,87,99,45,123] #test list
list_response = [] #placeholder list
for l in list: #apply look up to list
    #print(l)
    for l2 in buckets_2:
        #print(l2)
        if l2[0] <= l and l < l2[1]:
            list_response.append([l,l2[1]])
print("list reponse",list_response)
#list comprehension style
list_resp2 = [[l, l2[1]] for l in list for l2 in buckets_2 if l2[0] <= l & l < l2[1]]
print('list response 2',list_resp2)

#apply bucket to a series
test_s = pd.Series([2,3,4,60,70,89,45,23]) #test series
test_response = [] #placeholder list
for i in test_s: #apply look up to series
    #print(i)
    for l2 in buckets_2:
        if l2[0] <= i and i <l2[1]:
            test_response.append([i, l2[1]])
print('test response', test_response)
#list comprehension style
test_resp2 = [[i, l2[1]] for i in test_s for l2 in buckets_2 if l2[0] <= i & i < l2[1]]
print('test response 2', test_resp2)

#apply bucket to a dataframe
dict = {'VALUES':test_s,}
test_df = pd.DataFrame(data=dict)
test_df['BUCKET'] = None
print('set up df', test_df)
test_df2 = pd.DataFrame(data=dict)
test_df2['BUCKET'] = None
print('set up df2', test_df2)
#apply to df with for loop
for i in range(len(test_df['VALUES'])):
    print(test_df.loc[i, 'VALUES'])
    print(test_df.loc[i, 'BUCKET'])
    for l2 in buckets_2:
        #print(l2)
        if l2[0] <= test_df.loc[i, 'VALUES'] and test_df.loc[i, 'VALUES'] < l2[1]:
            test_df.loc[i, 'BUCKET'] = l2[1]
print('modified df',test_df)
#list comprehension style
test_df2['BUCKET'] = [l2[1] for i in range(len(test_df2)) for l2 in buckets_2 if l2[0] <= test_df2.loc[i, 'VALUES'] & test_df2.loc[i, 'VALUES'] < l2[1]]
print('modified df2', test_df2)

"""

''''
#didn't use
Series.between(left, right, inclusive=True)[source]
Return boolean Series equivalent to left <= series <= right.

'''
