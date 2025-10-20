import pandas as pd
from collections import Counter

def apply_layout(df: pd.DataFrame) -> pd.DataFrame:

    if 'memory_modules' not in df.columns:
        raise ValueError("DataFrame must contain a 'memory_modules' column")
    
    def format_memory(mem_str):
        # split by space
        vals = mem_str.split()
        # count occurrences
        counts = Counter(vals)
        # format as 'NxVALUE', preserve original order of first appearance
        formatted = []
        seen = set()
        for val in vals:
            if val not in seen:
                formatted.append(f"{counts[val]}x{val}")
                seen.add(val)
        return ' '.join(formatted)
    
    df = df.copy()
    df['memory_modules'] = df['memory_modules'].fillna('0 0 0 0')  # optional default
    df['memory_modules'] = df['memory_modules'].apply(format_memory)
    
    return df
