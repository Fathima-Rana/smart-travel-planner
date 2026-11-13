import pandas as pd
from pathlib import Path

# Get the project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Dataset location
DATA_PATH = PROJECT_DIR / "data" / "destinations.csv"


def load_data():
    """Load the destination dataset."""
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded successfully!")
    return df


def clean_data(df):
    """Clean and validate the destination data."""
    df = df.copy()

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean text columns
    text_columns = [
        "destination",
        "state",
        "category",
        "ideal_for",
        "best_season",
        "description",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Convert numeric columns
    df["estimated_daily_budget"] = pd.to_numeric(
        df["estimated_daily_budget"], errors="coerce"
    )

    df["minimum_days"] = pd.to_numeric(
        df["minimum_days"], errors="coerce"
    )

    # Remove rows missing essential values
    df = df.dropna(
        subset=[
            "destination",
            "state",
            "category",
            "estimated_daily_budget",
            "minimum_days",
        ]
    )

    # Remove invalid budgets and durations
    df = df[
        (df["estimated_daily_budget"] > 0)
        & (df["minimum_days"] > 0)
    ]

    # Convert numeric values to integers
    df["estimated_daily_budget"] = (
        df["estimated_daily_budget"].astype(int)
    )

    df["minimum_days"] = df["minimum_days"].astype(int)

    return df.reset_index(drop=True)


def main():
    # Load original dataset
    df = load_data()

    print("\nOriginal dataset shape:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    # Clean the dataset
    cleaned_df = clean_data(df)

    print("\nCleaned dataset shape:", cleaned_df.shape)

    print("\nFirst five cleaned destinations:")
    print(cleaned_df.head().to_string(index=False))

    # Save cleaned dataset
    output_path = (
        PROJECT_DIR / "data" / "destinations_cleaned.csv"
    )

    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved successfully!")
    print(output_path)


if __name__ == "__main__":
    main()