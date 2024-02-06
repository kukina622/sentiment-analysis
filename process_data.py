import json
import os
import time
from usecase import sentiment
from tqdm import tqdm

g_filename = None

def procrss_article(article):
  global g_filename

  total = {
    "negative": 0,
    "positive": 0
  }

  article_title_sentiment = sentiment.analysis(article["article_title"][0:512])[0]
  content_sentiment = sentiment.analysis(article["content"][0:512])[0]

  article["article_title_sentiment"] = article_title_sentiment["label"]
  article["content_sentiment"] = content_sentiment["label"]

  article["article_title_sentiment_score"] = article_title_sentiment["score"]
  article["content_sentiment_score"] = content_sentiment["score"]

  total[article_title_sentiment["label"]] += 1
  total[content_sentiment["label"]] += 1

  for message in article["messages"]:
    push_content_sentiment = sentiment.analysis(message["push_content"][0:512])[0]
    message["push_content_sentiment"] = push_content_sentiment["label"]
    message["push_content_sentiment_score"] = push_content_sentiment["score"]
    total[push_content_sentiment["label"]] +=1

  article["sentiment_count"] = total
  

start = time.time()
dataset_folder = "./dataset"
results_folder = "./results"

sentiment.load_model()
filenames = os.listdir(dataset_folder)
finish_filenames = os.listdir(results_folder)

filenames = [filename for filename in filenames if filename not in finish_filenames]
filenames = sorted(filenames, key=lambda x: int(x.split("-")[1]))

for filename in filenames:
  g_filename = filename
  data = None
  try:
      with open(f'{dataset_folder}/{filename}', "r", encoding="utf-8") as f:
        data = json.load(f)
  except:
    print(filename)
    continue
  
  for article in tqdm(data["articles"], desc=filename):
    try:
      procrss_article(article)
    except:
      continue
  
  if not os.path.exists(results_folder):
    os.makedirs(results_folder)
  
  with open(f'{results_folder}/{filename}', 'w', newline='', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

  end = time.time()
  print("執行時間：%f 秒" % (end - start))
