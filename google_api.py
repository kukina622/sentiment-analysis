import pandas as pd
from google.cloud import language_v2

df1 = pd.read_excel("./politics.xlsx")

client = language_v2.LanguageServiceClient()

def process(df):
  df['text'] = df['text'].astype(str)

  google_raw_score = []
  google = []

  for ind in df.index:
    document = language_v2.types.Document(
      content=df['text'][ind], type_=language_v2.types.Document.Type.PLAIN_TEXT,
      language_code='zh-Hant'
    )
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment
    google_raw_score.append(sentiment.score)
    google.append(0 if sentiment.score < 0 else 1)

  df['google raw score'] = google_raw_score
  df['google'] = google


process(df1)
df1.to_excel("politics_update.xlsx", index=False)