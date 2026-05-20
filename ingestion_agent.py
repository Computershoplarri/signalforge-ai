import pandas as pd

def load_data():

    df = pd.read_csv("data.csv")

    with open("supplier_report.txt") as f:
        supplier = f.read().lower()

    with open("complaints.txt") as f:
        complaints = f.read().lower()

    return df, supplier, complaints