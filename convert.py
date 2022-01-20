import pandas as pd
# df_ew = pd.read_excel('EW2020.xlsx')
# df_ew.drop(0,inplace=True)
# print(df_ew.head())
# df_ew.to_csv("EW2020.csv",index = False)

df_ew = pd.read_excel('Einwohner_Landkreise.xlsx')
df_ew.drop(0,inplace=True)
print(df_ew.head())
df_ew.to_csv("Einwohner_Landkreise.csv",index = False)