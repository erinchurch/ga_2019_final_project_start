import pandas as pd
import glob

class GetData():

    def get_acq_loans(self, fname):
        # usecols=filter_columns
        # nrows=1000
        df = pd.read_csv(fname, sep=",")
        return df

    def get_perf_loans(self,fname):
        # usecols=filter_columns
        # nrows=1000
        df = pd.read_csv(fname, sep=',')
        return df

    def merge(self, df1, df2):
        df_new = pd.merge(df1, df2, on='LOAN IDENTIFIER', validate='m:1' )
        return df_new

def main():
    # files = glob.glob('draft_multi_file_data/*')
    # print(files)
    #get data
    y = GetData()
    acq_in_file = 'draft_multi_file_data/acq_file_all.csv'
    a = GetData.get_acq_loans(y, acq_in_file)
    #source_acq = acq_in_file.replace('../draft_multi_file_data.','')
    #a['SOURCE_ACQ'] = source_acq
    print(a.head())
    print(a.shape)
    print(a.columns)
    perf_in_file = 'draft_multi_file_data/perf_file_all.csv'
    b = GetData.get_perf_loans(y, perf_in_file)
    #source_perf = perf_in_file.replace('../Performance_All/some-performance/', '')
    #b['SOURCE_PERF'] = source_perf
    print(b.head())
    print(b.shape)
    print(b.columns)
    # a.to_csv('draft_merge_data/sample_acq_data.csv')
    # b.to_csv('draft_merge_data/sample_perf_data.csv')

    #merge data
    c = GetData.merge(y, b, a)
    print(c.shape)
    print(c.columns)
    c.to_csv('draft_merge_data/perf_acq_data.csv')


if __name__ =='__main__':
    main()
