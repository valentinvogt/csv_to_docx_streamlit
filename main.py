import pandas as pd
from src.parse_docx import parse_docx, adapt_data
import os
import glob

# loop over files in directory sample_data
files = glob.glob("sample_data/*.docx")

for f in files:
    status, data = parse_docx(f, False)
    if status != "OK":
        print(status)
        exit()

    df = adapt_data(data)
    df.to_csv(os.path.join("sample_data", f"{os.path.basename(f).replace('.docx', '.csv')}"), index=False)
    print(f"Converted {f} to CSV.")
