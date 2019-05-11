import pandas as pd

"""


"""



def read_files(fname):

   df_columns = pd.read_csv('performance_file_headers.txt', sep=',')
   columns = df_columns['Field Name']
   #print(columns)
   #print(type(columns))
   headers = columns.tolist()
   #print(headers)


   df = pd.read_csv(fname, sep='|', header=None, names=headers, nrows=1000)

   return df


def main():
    a = 'Performance_2018Q1.txt'
    b = read_files(a)
    print(b.head())
    # c = 'Performance_2017Q4.txt'
    # d = read_files(c)
    # print(d.head())
    # e = 'Performance_2016Q4.txt'
    # f = read_files(e)
    # print(f.head())
    # g = 'Performance_2015Q4.txt'
    # h = read_files(g)
    # print(h.head())

main()

# df_columns = pd.read_csv('performance_file_headers.txt', sep=',')
# print(df_columns.columns)
# columns = df_columns['Field Name']
# print(columns)
