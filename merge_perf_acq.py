import pandas as pd

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


    def merge(self, df1, df2):
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
    #merge data
    c = GetData.merge(y, b, a)
    print(c.shape)
    print(c.columns)
    c.to_csv('sample_perf_acq_data.csv')


if __name__ =='__main__':
    main()
