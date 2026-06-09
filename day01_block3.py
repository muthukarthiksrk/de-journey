import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def extract(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, skipinitialspace=True)
        logging.info(f"Extracted {len(df)} rows from {filepath}")
        return df
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return pd.DataFrame()

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df_filtered = df[df["status"] == "completed"].copy()
    df_filtered["tax"] = df_filtered["amount"] * 0.18
    df_filtered["total"] = df_filtered["amount"] + df_filtered["tax"]
    logging.info(f"Transformed: {len(df_filtered)} rows after filter")
    return df_filtered

def load(df: pd.DataFrame, filepath: str):
    try:
        df.to_csv(filepath, index=False)
        logging.info(f"Loaded {len(df)} rows to {filepath}")
    except Exception as e:
        logging.error(f"Load failed: {e}")

def run_pipeline():
    logging.info("Pipeline started")
    df_raw = extract("sales.csv")
    df_clean = transform(df_raw)
    load(df_clean, "sales_clean.csv")
    print(df_clean)
    logging.info("Pipeline completed!")

run_pipeline()