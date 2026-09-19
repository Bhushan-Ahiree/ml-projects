import pandas as pd


def clean_house_size(size_str: str) -> float:
    cleaned = size_str.replace(",", "")
    cleaned = cleaned.replace("sq ft", "")
    cleaned = cleaned.strip()
    return float(cleaned)


def add_ids(df: pd.DataFrame, city: str) -> pd.DataFrame:
    df = df.copy()
    df["id"] = city + "_" + df.index.astype(str)
    return df


def load_raw_csv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    columns_to_drop = [
        "currency",
        "numBalconies",
        "isNegotiable",
        "priceSqFt",
        "latitude",
        "longitude",
        "verificationDate",
    ]
    columns_to_drop = [c for c in columns_to_drop if c in df.columns]
    df = df.drop(columns=columns_to_drop, errors="ignore")
    return df


# compatibility alias for older notebook imports
infilter_columns = filter_columns