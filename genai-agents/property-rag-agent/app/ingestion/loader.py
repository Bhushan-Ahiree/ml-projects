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


def drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=["numBathrooms", "description"])
    return df


def process_city(filepath: str, city: str) -> pd.DataFrame:
    df = load_raw_csv(filepath)
    df = filter_columns(df)
    df = drop_incomplete_rows(df)
    df["house_size"] = df["house_size"].apply(clean_house_size)
    df = fix_city(df, city)
    df = add_ids(df, city)
    return df


def fix_city(df: pd.DataFrame, city: str) -> pd.DataFrame:
    df = df.copy()
    df["city"] = city
    return df


def save_processed(df: pd.DataFrame, output_path: str) -> None:
    df.to_json(output_path, orient="records", lines=True)
    
    
def load_all_properties(raw_dir: str) -> pd.DataFrame:
    delhi = process_city(f"{raw_dir}/Indian_housing_Delhi_data.csv", "Delhi")
    mumbai = process_city(f"{raw_dir}/Indian_housing_Mumbai_data.csv", "Mumbai")
    pune = process_city(f"{raw_dir}/Indian_housing_Pune_data.csv", "Pune")

    df = pd.concat([delhi, mumbai, pune], ignore_index=False)

    return df