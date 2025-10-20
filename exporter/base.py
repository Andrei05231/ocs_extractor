from abc import ABC, abstractmethod
import pandas as pd

class BaseExporter(ABC):
    @abstractmethod
    def export(self, df: pd.DataFrame, filename:str):
            pass
