import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import sys
import re

# Path to your data folder
DATA_FOLDER = Path(__file__).parent / "data"

def sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names to be compatible with BigQuery:
    - Replace spaces with underscores
    - Remove special characters
    - Optionally replace $ with USD
    """
    new_columns = []
    for col in df.columns:
        col_clean = col.strip()
        col_clean = col_clean.replace("$", "USD")           # replace $ with USD
        col_clean = re.sub(r"[^\w]", "_", col_clean)       # replace any non-alphanumeric/_ with _
        col_clean = re.sub(r"_+", "_", col_clean)          # collapse multiple underscores
        col_clean = col_clean.strip("_")                   # remove leading/trailing underscores
        new_columns.append(col_clean)
    df.columns = new_columns
    return df

def split_csv(filename, test_size=0.2):
    """
    Split CSV into train/test sets and save them in data/
    
    Args:
        filename (str): CSV filename located in data/
        test_size (float): fraction of data to use as test set
    """
    input_path = DATA_FOLDER / filename
    train_path = DATA_FOLDER / "train.csv"
    test_path = DATA_FOLDER / "test.csv"

    # Check if input CSV exists
    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} does not exist.")

    # Load data
    df = pd.read_csv(input_path)

    # Sanitize column names for BigQuery
    df = sanitize_columns(df)

    # Split dataset
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

    # Save outputs
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Saved {len(train_df)} rows to {train_path}")
    print(f"Saved {len(test_df)} rows to {test_path}")


# Run only when executing this script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_preprocessing.py <csv_filename>")
        sys.exit(1)
    
    csv_filename = sys.argv[1]  # get filename from terminal argument
    split_csv(csv_filename)
