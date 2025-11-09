from flask import Flask, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)
DATA_PATH = Path(__file__).resolve().parents[1]  / "data/Restaurant reviews.csv"

def process_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df.dropna(subset=['Restaurant', 'Rating'], inplace=True)

    def get_sentiment(text):
        if pd.isna(text):
            return 'Neutral'
        t = str(text).lower()
        if any(w in t for w in ['good', 'great', 'excellent']):
            return 'Positive'
        if any(w in t for w in ['bad', 'poor', 'terrible']):
            return 'Negative'
        return 'Neutral'

    df['Sentiment'] = df['Review'].apply(get_sentiment)

    top5 = (df.groupby('Restaurant')['Rating']
              .mean()
              .sort_values(ascending=False)
              .head(5)
              .reset_index())

    sentiment_count = df['Sentiment'].value_counts().to_dict()
    return df, top5, sentiment_count

@app.route('/api/top5')
def top5():
    _, top5, _ = process_data()
    return jsonify(top5.to_dict(orient='records'))

@app.route('/api/sentiment')
def sentiment():
    _, _, s = process_data()
    return jsonify(s)

@app.route('/api/raw')
def raw():
    df, _, _ = process_data()
    return jsonify(df.head(100).to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)  # đổi port nếu cần
