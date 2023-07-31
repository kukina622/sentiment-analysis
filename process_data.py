import json
import os
import time
from usecase import sentiment


def procrss_article(article, article_idx, all_article_count):
  total = {
    "negative": 0,
    "positive": 0
  }

  article_title_sentiment = sentiment.analysis(article["article_title"][0:512])[0]
  content_sentiment = sentiment.analysis(article["content"][0:512])[0]

  article["article_title_sentiment"] = article_title_sentiment
  article["content_sentiment"] = content_sentiment

  total[article_title_sentiment] += 1
  total[content_sentiment] += 1

  messages_length = len(article['messages'])
  for idx, message in enumerate(article["messages"]):
    print(
      f"article: {article_idx+1}/{all_article_count}, message: {idx+1}/{messages_length}"
    )
    push_content_sentiment = sentiment.analysis(message["push_content"][0:512])[0]
    message["push_content_sentiment"] = push_content_sentiment
    total[push_content_sentiment] +=1

  article["sentiment_count"] = total


start = time.time()
dataset_folder = "./dataset"
sentiment.load_model()
filenames = os.listdir(dataset_folder)
filenames = sorted(filenames, key=lambda x: int(x.split("-")[1]))

for filename in filenames:
  data = None
  try:
      with open(f'{dataset_folder}/{filename}', "r", encoding="utf-8") as f:
        data = json.load(f)
  except:
    print(filename)
    continue
  
  all_article_count = len(data["articles"])
  for idx, article in enumerate(data["articles"]):
    try:
      procrss_article(article, idx, all_article_count)
    except:
      continue
  
  if not os.path.exists("results"):
    os.makedirs("results")
  
  with open(f'./results/{filename}', 'w', newline='', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

  end = time.time()
  print("執行時間：%f 秒" % (end - start))
