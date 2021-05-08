import pandas
      
df=pandas.read_csv("dataImmo.csv", sep=';',encoding="utf-8-sig",dtype={'Code-Postal':str})
#print(df.sort_values(by='Code-Postal'))

df01=df[df['Code-Postal'].str[:2]=="71"]

for num in range(1,96):
    numd=str(num)
    if num<10:
        numd='0'+str(num)
    df_dep=df[df['Code-Postal'].str[:2]==numd]
    nom_csv="dep_"+numd+".csv"
    df_dep.to_csv(nom_csv, sep=';',encoding="utf-8-sig",index=None)
