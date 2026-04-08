import pandas as pd
import warnings

warnings.filterwarnings('ignore')

try:
    df1 = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrement  catégorisation vocb base/bd.xlsx')
    print("Cat Base Unique Categories:", df1['category'].unique().tolist())
except Exception as e: print("df1 err:", e)

try:
    df2 = pd.read_excel('bd_final/enregistrement vocab riche/catégorisation/bd.xltx')
    print("Cat Rich Unique Categories:", df2['category'].unique().tolist())
except Exception as e: print("df2 err:", e)

try:
    df3 = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrements discrimination vocabulaire de base/enregistrement discrimination/db.xltx')
    print("Disc Base Unique Contrasts:", df3['category'].unique().tolist())
    print("Disc Base Unique Phonemes:", df3['category1'].unique().tolist())
except Exception as e: print("df3 err:", e)

try:
    df4 = pd.read_excel('bd_final/enregistrement vocab riche/discrimination/bd.ods', engine='odf')
    print("Disc Rich Unique Contrasts:", df4['category'].unique().tolist())
    print("Disc Rich Unique Phonemes:", df4['category1'].unique().tolist())
except Exception as e: print("df4 err:", e)
