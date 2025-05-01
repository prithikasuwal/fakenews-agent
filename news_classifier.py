import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import os
import joblib

DATASET_PATH = os.path.join("data", "AiSummitArticles.csv")
MODEL_PATH = os.path.join("data", "news_classifier.joblib")

# Column names for text and label in your CSV
def get_text_and_label_columns(df):
    # Try to find the text column (prefer 'Article Name', fallback to first column)
    text_col = 'Article Name' if 'Article Name' in df.columns else df.columns[0]
    label_col = 'Type' if 'Type' in df.columns else df.columns[-1]
    return text_col, label_col

def train_and_save_model(csv_path=DATASET_PATH, model_path=MODEL_PATH):
    df = pd.read_csv(csv_path)
    text_col, label_col = get_text_and_label_columns(df)
    X = df[text_col].astype(str)
    y = df[label_col].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_path)
    acc = pipeline.score(X_test, y_test)
    print(f"Model trained and saved to {model_path}. Test accuracy: {acc:.2f}")
    return acc

def load_model(model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train it first.")
    return joblib.load(model_path)

def predict_article_type(article_text, model_path=MODEL_PATH):
    model = load_model(model_path)
    pred = model.predict([article_text])[0]
    return pred

if __name__ == "__main__":
    # Train the model if run as a script
    train_and_save_model()
