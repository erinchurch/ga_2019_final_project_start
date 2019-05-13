#taken from homework
#actual pd printing never worked


import pandas as pd
import datetime as dt
#import numpy as np #not using
#import matplotlib #not using
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#plotting works, writing to pdf does not yet work

def get_byVintage(fname):
    #index_col='VINTAGE',
    byVintage = pd.read_csv(fname, sep=",",)
    return byVintage



def scatter_plot_byVintage(dfname, x, y, title,):
    scatter = plt.scatter(dfname[x], dfname[y], color = 'green')
    plt.title(title, fontsize = 12)
    plt.xlabel(x, fontsize = 10)
    plt.ylabel(y, fontsize = 10)
    plt.grid(True)
    plt.show()
    return scatter

def line_chart_byVintage(dfname, x, y, title):
    zplot = plt.plot(dfname[x], dfname[y], color = 'green')
    plt.title(title, fontsize = 12)
    plt.xlabel(x, fontsize = 10)
    plt.ylabel(y, fontsize = 10)
    plt.grid(True)
    plt.show()
    return zplot


# def line_chart_pdf(dfname, x, y, title, fname, note, dict): #doesn't work
#     with PdfPages(fname) as pdf:
#         plt.rc('text', usetex=True)
#         plt.figure(figsize=(3, 3))
#         plt.plot(dfname[x], dfname[y], color = 'green')
#         plt.title(title, fontsize = 12)
#         plt.xlabel(x, fontsize = 10)
#         plt.ylabel(y, fontsize = 10)
#         plt.grid(True)
#         plt.show()
#         pdf.savefig()
#         plt.close()
#         pdf.attach_note(note)
#         dict = pdf.infodict()
#         return


# def plot_to_pdf(fname, a, b, dict, note):
#     with PdfPages(fname) as pdf:
#         pdf.attach_note(note)
#         dict = pdf.infodict()
#         a = plt.figure()
#         pdf.savefig(a)
#         plt.close()
#         b = plt.figure()
#         pdf.savefig(b)
#         plt.close()


# def plot_to_pdf(fname, dict, note): #doesn't work
#     with PdfPages(fname) as pdf:
#         pdf.attach_note(note)
#         dict = pdf.infodict()
#         plt.figure(figsize=(3, 3))
#         scatter = scatter_plot_byVintage(byVintage, 'VINTAGE', 'Loan Count', 'Vintage vs. Loan Count')
#         pdf.savefig(scatter)
#         plt.close(scatter)
#         plt.figure(figsize=(3, 3))
#         line_chart = line_chart_byVintage(byVintage, 'VINTAGE', 'Loan Count', 'Loan Count by Vintage')
#         pdf.savefig(line_chart)
#         plt.close(line_chart)



def dict_for_pdf(title, author, subject, keywords):
    now = dt.datetime.now()
    today = dt.datetime.today()
    d = {}
    d['Title'] = title
    d['Author'] = author
    d['Subject'] = subject
    d['Keywords'] = keywords
    d['CreationDate'] = now
    d['ModDate'] = today
    return d


#these work
byVintage  = get_byVintage('acq_files_analysis/Acq_byVintage.csv')
print(byVintage)
scatter_byVintage = scatter_plot_byVintage(byVintage, 'VINTAGE', 'Loan Count', 'Vintage vs. Loan Count')
line_chart_byVintage = line_chart_byVintage(byVintage, 'VINTAGE', 'Loan Count', 'Loan Count by Vintage')
dict = dict_for_pdf('Practive with Python PDF Charting', 'Erin Church', 'FNMA Acquistion Data', 'Mortgage Data, FNMA, PDF')
note = 'FNMA Acquisition Data thru 2018Q1'
#can't get the pdf writing part to work

#line_chart_Vintage_pdf = line_chart_pdf(byVintage, 'VINTAGE', 'Loan Count', 'Loan Count by Vintage', 'acq_files_analysis/charts.pdf', note, dict)
#pdf = plot_to_pdf('acq_files_analysis/charts.pdf', dict, note)


# scatter_view_byVintage = scatter_plot_view_only(byVintage, 'VINTAGE', 'Loan Count', 'Vintage vs. Loan Count')
# line_chart_view_byVintage = line_chart_view_only(byVintage, 'VINTAGE', 'Loan Count', 'Loan Count by Vintage')


# plt.scatter(df1['Unemployment_Rate'], df1['Stock_Index_Price'], color='green')
# plt.title('Unemployment Rate Vs Stock Index Price', fontsize=14)
# plt.xlabel('Unemployment Rate', fontsize=14)
# plt.ylabel('Stock Index Price', fontsize=14)
# plt.grid(True)
# plt.show()