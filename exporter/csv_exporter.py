import pandas as pd
from .base import BaseExporter

class CSVExporter(BaseExporter):
    def export(self, df: pd.DataFrame, filename:str):
        df.to_csv(filename, index=False)
        print(f"CSV exported: {filename}")
