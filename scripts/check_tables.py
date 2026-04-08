import pandas as pd
import sys
import glob

def print_head(path):
    print(f"\n--- {path} ---")
    try:
        df = pd.read_excel(path)
        print("Columns:", df.columns.tolist())
        print(df.head(2))
    except Exception as e:
        print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    for f in glob.glob('bd_final/**/*.xls*', recursive=True) + glob.glob('bd_final/**/*.ods', recursive=True):
        print_head(f)
