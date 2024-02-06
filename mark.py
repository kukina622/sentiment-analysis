import pandas as pd
from usecase import sentiment

pipe = sentiment.load_model()

df1 = pd.read_excel("./politics_google.xlsx")


def process(df):
  df_text = [str(x)[:512] for x in df["text"].to_list()]
  result = list(map(lambda x: 0 if x["label"] == "LABEL_0" else 1, pipe(df_text)))
  df["our model"] = result

process(df1)
df1.to_excel("politics_google_update.xlsx", index=False)
