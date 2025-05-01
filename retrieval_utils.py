import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_top_k_similar_articles(df, query_text, text_col='Article Name', k=3):
    """
    Returns the top k most similar articles to query_text from df, using TF-IDF cosine similarity.
    Returns a list of (index, similarity, row) tuples.
    """
    texts = df[text_col].astype(str).tolist()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts + [query_text])
    query_vec = tfidf_matrix[-1]
    similarities = cosine_similarity(query_vec, tfidf_matrix[:-1]).flatten()
    top_k_idx = similarities.argsort()[::-1][:k]
    results = []
    for idx in top_k_idx:
        sim = similarities[idx]
        row = df.iloc[idx]
        results.append((idx, sim, row))
    return results
