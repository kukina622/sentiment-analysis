import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, BertTokenizerFast
from .util import traditional_to_simplified_chinese

model_folder_path = os.path.join(os.path.dirname(__file__), '..', 'model')
pipe = None


def load_model():
  global pipe
  tokenizer = BertTokenizerFast.from_pretrained("ckiplab/bert-base-chinese")
  model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)
  pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)
  return pipe


def label_mapping(model_results):
  mapping_func = lambda y: {**y , "label": "negative"} if y["label"] == "LABEL_0" else  {**y , "label": "positive"}
  return list(map(mapping_func, model_results))


def analysis(texts: str | list[str]) -> str | list[str]:
  model_results = pipe(texts)
  return label_mapping(model_results)
