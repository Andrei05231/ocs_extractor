import pandas as pd
from collections import Counter
from typing import Callable, Dict


# --- Define individual filter functions ---

def format_memory_modules(df: pd.DataFrame) -> pd.DataFrame:
    """Formats memory modules like '8GB 8GB 16GB' -> '2x8GB 1x16GB'."""
    if 'memory_modules' not in df.columns:
        return df

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

    df = df.copy()
    df['memory_modules'] = df['memory_modules'].fillna('0 0 0 0')
    df['memory_modules'] = df['memory_modules'].apply(format_memory)
    return df


def reverse_gpus(df: pd.DataFrame) -> pd.DataFrame:
    """Reverses GPU order to show discrete GPUs first."""
    if 'gpus' not in df.columns:
        return df

    def reverse_gpus(gpu_str):
        if not gpu_str or gpu_str.strip() == '':
            return ''
        gpu_list = [g.strip() for g in gpu_str.split(',')]
        gpu_list.reverse()
        return ', '.join(gpu_list)

    df = df.copy()
    df['gpus'] = df['gpus'].apply(reverse_gpus)
    return df


# --- Core layout function ---

def apply_layout(df: pd.DataFrame, enabled_filters: Dict[str, bool] = None) -> pd.DataFrame:
    """Applies a sequence of enabled filters to the DataFrame."""
    df = df.copy()

    # Registry of available filters
    filters: Dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
        'format_memory': format_memory_modules,
        'reverse_gpus': reverse_gpus,
    }

    # Default: all filters enabled
    if enabled_filters is None:
        enabled_filters = {name: True for name in filters}

    # Apply only enabled filters
    for name, func in filters.items():
        if enabled_filters.get(name, False):
            df = func(df)

    return df
