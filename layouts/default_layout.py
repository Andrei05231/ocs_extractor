import pandas as pd
from collections import Counter

def apply_layout(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    
    # --- Memory formatting ---
    if 'memory_modules' in df.columns:
        def format_memory(mem_str):
            vals = mem_str.split()
            counts = Counter(vals)
            formatted = []
            seen = set()
            for val in vals:
                if val not in seen:
                    formatted.append(f"{counts[val]}x{val}")
                    seen.add(val)
            return ' '.join(formatted)
        
        df['memory_modules'] = df['memory_modules'].fillna('0 0 0 0')
        df['memory_modules'] = df['memory_modules'].apply(format_memory)
    
    # --- Reverse GPU order to show descrete first--
    if 'gpus' in df.columns:
        def reverse_gpus(gpu_str):
            if not gpu_str or gpu_str.strip() == '':
                return ''
            gpu_list = [g.strip() for g in gpu_str.split(',')]
            gpu_list.reverse()  # reverse the order
            return ', '.join(gpu_list)
        
        df['gpus'] = df['gpus'].apply(reverse_gpus)
    
    return df
