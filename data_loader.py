import pandas as pd
import os

# Path to the dataset
DATASET_PATH = os.path.join("data", "AiSummitArticles.csv")


def load_articles_dataset(path=DATASET_PATH):
    """
    Loads the AiSummitArticles.csv dataset into a pandas DataFrame.
    Returns the DataFrame, or raises FileNotFoundError if not found.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    df = pd.read_csv(path)
    return df


def categorize_articles(df, label_column="Type"):
    """
    Categorizes articles based on their label column ('Type' by default).
    Returns a dictionary with label as key and list of articles as value.
    """
    if label_column not in df.columns:
        raise ValueError(f"Label column '{label_column}' not found in DataFrame.")
    categories = df[label_column].unique()
    categorized = {cat: df[df[label_column] == cat] for cat in categories}
    return categorized

# Example usage (uncomment to test):
# df = load_articles_dataset()
# categorized = categorize_articles(df)
# print({k: len(v) for k, v in categorized.items()})
