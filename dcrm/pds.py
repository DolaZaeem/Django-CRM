import pandas as pd
file = 'C:/Users/ZM/Desktop/Data.xlsx'

workbook = pd.read_excel(file,sheet_name=['Sheet1','Sheet2'],header=0)
sheet1 = workbook['Sheet1'].values[0,3]
sheet2 = workbook['Sheet2'].values

new =pd.to_datetime(sheet1,yearfirst=1)
print(new)