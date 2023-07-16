import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from .util import traditional_to_simplified_chinese

model_name = 'hfl/chinese-roberta-wwm-ext'
model_folder_path = os.path.join(os.path.dirname(__file__), '..', 'model')
pipe = None


def load_model():
  global pipe
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForSequenceClassification.from_pretrained(model_folder_path)
  pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)


def label_mapping(model_results):
  mapping_func = lambda y: "negative" if y["label"] == "LABEL_0" else "positive"
  return list(map(mapping_func, model_results))


def analysis(texts: str | list[str]) -> str | list[str]:
  texts = traditional_to_simplified_chinese(texts)
  model_results = pipe(texts)
  return label_mapping(model_results)
