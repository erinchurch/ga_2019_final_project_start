import pandas as pd
import glob


class GetDataMultiFile():

    def files_acq_to_df(self, fname):
        df_columns = pd.read_csv("../FNMA-raw-data/some-acquisition-dev/header_aquisition_file.txt", sep=",")
        columns = df_columns['Field Name']
        headers = columns.tolist()
        filter_columns = ['LOAN IDENTIFIER', 'ORIGINAL INTEREST RATE', 'ORIGINAL UPB',
                          'ORIGINATION DATE', 'ORIGINAL LOAN-TO-VALUE (LTV)',
                          'ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)', 'ORIGINAL DEBT TO INCOME RATIO',
                          'BORROWER CREDIT SCORE AT ORIGINATION', 'CO-BORROWER CREDIT SCORE AT ORIGINATION']
        # TO FILTER FOR SPEED, nrows=1000, FILTERED FOR 1000 ROWS, TURN THAT OFF FOR FINAL SUBMISSION
        #usecols=filter_columns,
        # index = 'LOAN IDENTIFIER'
        # index_col = index
        #nrows =
        df = pd.read_csv(fname, sep="|", header=None, names=headers,nrows=100000)
        return df


    def files_perf_to_df(self,fname):
        df_columns = pd.read_csv('../FNMA-raw-data/some-performance-dev/performance_file_headers.txt', sep=',')
        columns = df_columns['Field Name']
        headers = columns.tolist()
        # TO FILTER FOR SPEED, nrows=1000, FILTERED FOR 1000 ROWS, TURN THAT OFF FOR FINAL SUBMISSION
        # usecols=filter_columns
        # index = 'LOAN IDENTIFIER'
        # index_col = index
        # nrows=1000
        df = pd.read_csv(fname, sep='|', header=None, names=headers,nrows=100000)
        return df

    def df_to_files(self, df_name, fname):
        df_name.to_csv(fname, sep=',')
        return


class ProcessFiles():
    def acq_files(self):
        x = GetDataMultiFile()
        files_acq = glob.glob('../FNMA-raw-data/some-acquisition/*')
        dfs = []
        for file in files_acq:
            name = file.replace('../FNMA-raw-data/some-acquisition/', '')
            print(name)
            df = GetDataMultiFile.files_acq_to_df(x, file)
            df['SOURCE'] = name
            print(df.head())
            dfs.append(df)
        df_all = pd.concat(dfs, axis=0, ignore_index=True)
        name_all = 'draft_multi_file_data/acq_file_02-03.csv'
        GetDataMultiFile.df_to_files(x, df_all, name_all)
        return df_all

    def perf_files(self):
        x = GetDataMultiFile()
        files_perf = glob.glob('../FNMA-raw-data/some-performance/*')
        dfs = []
        for file in files_perf:
            name = file.replace('../FNMA-raw-data/some-performance/', '')
            print(name)
            df = GetDataMultiFile.files_perf_to_df(x, file)
            df['SOURCE'] = name
            print(df.head())
            dfs.append(df)
        df_all = pd.concat(dfs, axis=0, ignore_index=True)
        name_all = 'draft_multi_file_data/perf_file_02-03.csv'
        GetDataMultiFile.df_to_files(x, df_all, name_all)
        return df_all


def main():

    w = ProcessFiles()
    df_all_acq = ProcessFiles.acq_files(w)
    print(df_all_acq.head())
    print(df_all_acq.tail())
    print(df_all_acq.shape)
    print(df_all_acq.columns)
    df_all_perf = ProcessFiles.perf_files(w)
    print(df_all_perf.head())
    print(df_all_perf.tail())
    print(df_all_perf.shape)
    print(df_all_perf.columns)

if __name__=='__main__':
    main()




