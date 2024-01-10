import pandas as pd

import io

def convert_csv_to_xlsx(csv_contents):
    df = pd.read_csv(io.StringIO(csv_contents.decode('utf-8')))
    xlsx_output = io.BytesIO()
    with pd.ExcelWriter(xlsx_output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    xlsx_output.seek(0)
    return xlsx_output

def convert_csv_to_xlsx_and_print(csv_contents):
    df = pd.read_csv(io.StringIO(csv_contents.decode('utf-8')))
    xlsx_output = io.BytesIO()
    with pd.ExcelWriter(xlsx_output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    xlsx_output.seek(0)
    
    # Reading XLSX sheet-wise and printing data
    xlsx_data = pd.read_excel(xlsx_output, sheet_name=None)
    for sheet_name, sheet_df in xlsx_data.items():
        print(f"Data from {sheet_name}:")
        print(sheet_df.to_string(index=False))
        print("\n")