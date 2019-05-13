import pandas as pd
import numpy as np

#refined from tagging_df_acqusition
#single file input version

class GetData():
    def read_acq_files(self, fname):
        acq_header_file = pd.read_csv('../Performance_All/some-acquisition/header_aquisition_file.txt', sep=",")
        # print("headers file", acq_header_file.head())

        columns = acq_header_file["Field Name"]
        # print("headers", columns)

        filter_columns = ['LOAN IDENTIFIER', 'ORIGINAL INTEREST RATE', 'ORIGINAL UPB',
                          'ORIGINATION DATE', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                          'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO',
                          'BORROWER CREDIT SCORE AT ORIGINATION', 'CO-BORROWER CREDIT SCORE AT ORIGINATION']
        # usecols=filter_columns
        # nrows=1000
        df = pd.read_csv(fname, sep="|", header=None, names=columns, infer_datetime_format=True,nrows=100000,)
        print(df.shape)
        print(df.columns)
        #print(df['ORIGINAL INTEREST RATE'].max())  #developer check
        #print(df['ORIGINAL INTEREST RATE'].min())  #developer check
        #print(df['ORIGINAL INTEREST RATE'].median())  #developer check
        #print(df['ORIGINAL INTEREST RATE'].head())
        return df

    def write_results(self, df, fname):
        df.to_csv(fname, sep=',')
        return


class DataTransform():

    def bucket_list_long(self, list_name, min, max, increment):
        # much slower
        base_list = np.arange(min, max, increment) #generate the bucket levels
        for x in base_list: #for bucket level in base list
            if x <= max: #if the bucket level is between in the min and max
                list_name += [[x, x+increment]]  #create the bounds the bucket
        return list_name  #give back the list containing bucket bounds

    def bucket_list(self, list_name, min, max, increment):  #same as bucket() but in list comprehension form
        base_list = np.arange(min, max, increment)  #generate the bucket levels
        list_name = [[x, x + increment] for x in base_list if x <= max] #generate the bucket range - WORKS
        return list_name


    def df_bucket_long(self, df, df_field, df_bucket_name, bucket_list):  #same as df_bucket_list_comp but in for loop form
        #much slower
        #not an integer centric function
        #df[df_bucket_name] = None #create the new bucket key field
        # print('check iterable length',len(df[df_field]))
        # print('check iterable length range', df.size)
        for i in range(len(df[df_field])):  #for value in df series
            #print(df.loc[i, df_field]) #developer check to print the value in the df series
            #print(df.loc[i, df_bucket_name]) #developer check to print the destination bucket value, should be None
            for b in bucket_list:  #for the bucket min, max in the bucket list provided
                # print(b) #developer check
                if b[0] <= df.loc[i, df_field] and df.loc[i, df_field] < b[1]:  #if the value in the df series is between the bucket list min, max
                    df.loc[i, df_bucket_name] = b[0]  #update the df bucket name value to be the value of the bucket max
        # print('modified df', df.head()) #developer check
        return df  #return the dataframe after update


    def df_bucket(self, df, df_field, df_derived, bucket_list):
        # data type of df series and buckets should match
        df[df_derived] = None
        df[df_derived] = [b[0] for i in range(len(df[df_field])) for b in bucket_list if b[0] <= df.loc[i, df_field] and df.loc[i, df_field] < b[1]]
        #print('modified df2 in df_bucket2 function\n', df.head())
        return df #return the dataframe after update


    def nan_fix(self, df, df_field, df_derived, enrich):
        df[df_field].to_csv(('pre-' + df_derived + '.csv'), sep=',')
        df[df_field].fillna(value=enrich, inplace=True)  #edit the data set and overwrite
        df[df_field].to_csv(('post-'+df_derived+'.csv'), sep=',')
        return df  # return the dataframe after update


    def count_long(self, df, x, y): #for loop style
        for i in df[x]:  #create a loan count number, to be groupedby later
            if i != 'NaN' or i != 0:
                df[y] = 1
            else:
                df[y] = 0
        return df


    def count(self, df, x, y): #list compression style
        df[y] = [1 for i in df[x] if i != 'NaN' or i != 0] #create a loan count number, to be groupedby later
        return df


    def vintage_yr(self, df, x, y):
        df[y] = pd.DatetimeIndex(df[x]).year #convert the data to a data format, apply year method.
        return df


    def vintage_mnth(self, df, x, y):
        df[y] = pd.DatetimeIndex(df[x]).month  #convert the data to a data format, apply month method.
        return df


class CallTransform():

    def derive_loan_count(self, df, df_field, df_derived):
        # loan count - WORKS
        loan_num = df_field
        loan_count = df_derived
        #acq_df_ln_ct = count_long(df, loan_num, loan_count) #long one, skip
        x = DataTransform()
        acq_df_ln_ct = DataTransform.count(x, df, loan_num, loan_count)
        print(acq_df_ln_ct.head())
        return acq_df_ln_ct


    def derive_vintage(self, df, df_field, df_derived_1, df_derived_2):
        x = DataTransform()
        df_y = DataTransform.vintage_yr(x, df, df_field, df_derived_1)
        print(df_y.head())
        df_m = DataTransform.vintage_mnth(x, df_y, df_field, df_derived_2)
        print(df_m.head())
        return df_m


    def derive_buckets(self, df, df_field, df_derived, bucket_min, bucket_max, bucket_incr, nan_enrich):
        #create buckets
        bucket_list = []
        x = DataTransform()
        df_fix = DataTransform.nan_fix(x, df, df_field, df_derived, nan_enrich)
        #print(df_fix.head())  #developer check
        bucket = DataTransform.bucket_list(x, bucket_list, bucket_min, bucket_max, bucket_incr)
        #print(bucket) #developer check
        #apply buckets
        df_buck = DataTransform.df_bucket(x, df_fix, df_field, df_derived, bucket)
        #df_buck = DataTransform.df_bucket_long(x, df_fix, df_field, df_derived, bucket) #long one
        print(df_buck.head())  #developer test
        return df_buck


def main():
    #get data WORKS
    y = GetData()
    z = CallTransform()
    in_file = '../Performance_All/some-acquisition/Acquisition_2017Q2.txt'
    a = GetData.read_acq_files(y, in_file)
    source = in_file.replace('../Performance_All/some-acquisition/','')
    a['SOURCE'] = source
    print(a.head())

    #loan count - WORKS
    loan_num = 'LOAN IDENTIFIER'
    loan_count = 'LOAN_COUNT'
    b = CallTransform.derive_loan_count(z, a, loan_num, loan_count)

    #vintage - WORKS
    orig_dt = 'ORIGINATION DATE'
    vintage_y = 'VINTAGE_YEAR'
    vintage_m = 'VINTAGE_MONTH'
    c = CallTransform.derive_vintage(z,b, orig_dt, vintage_y, vintage_m)

    #create buckets WORKS
    #LTV bucket
    ltv_min = 0
    ltv_max = 200
    ltv_incr = 10
    ltv_enrich = 80
    s_LTV = 'ORIGINAL LOAN-TO-VALUE (LTV)'
    b_LTV = 'LTV_BUCKET'
    d = CallTransform.derive_buckets(z, c, s_LTV, b_LTV, ltv_min, ltv_max, ltv_incr, ltv_enrich)

    #UPB bucket
    upb_min = 0
    upb_max = 2000000
    upb_incr = 50000
    upb_enrich = 200000
    s_UPB = 'ORIGINAL UPB'
    b_UPB = 'UPB_BUCKET'
    e = CallTransform.derive_buckets(z, d, s_UPB, b_UPB, upb_min, upb_max, upb_incr, upb_enrich)

    #FICO bucket
    fico_min = 300.0
    fico_max = 900.0
    fico_incr = 50.0
    fico_enrich = 750.0
    s_FICO = 'BORROWER CREDIT SCORE AT ORIGINATION'
    b_FICO = 'FICO_BUCKET'
    f = CallTransform.derive_buckets(z, e, s_FICO, b_FICO, fico_min, fico_max, fico_incr, fico_enrich)

    #TERM bucket
    term_min = 0
    term_max = 480
    term_incr = 60
    term_enrich = 360
    s_term = 'ORIGINAL LOAN TERM'
    b_term = 'TERM_BUCKET'
    g = CallTransform.derive_buckets(z, f, s_term, b_term, term_min, term_max, term_incr, term_enrich)

    #Interest Rate bucket
    int_rt_min = 0
    int_rt_max = 15
    int_rt_incr = 0.125
    int_rt_enrich = 4.25
    s_int_rt = 'ORIGINAL INTEREST RATE'
    b_int_rt = 'INT_RT_BUCKET'
    h = CallTransform.derive_buckets(z, g, s_int_rt, b_int_rt, int_rt_min, int_rt_max, int_rt_incr, int_rt_enrich)


    #write output file
    out_file = 'Acquisition_Out.csv'
    i = GetData.write_results(y, h, out_file)



if __name__ == '__main__':
    main()





