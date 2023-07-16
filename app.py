import uvicorn
from fastapi import FastAPI
from usecase import sentiment
from pydantic import BaseModel

app = FastAPI()
sentiment.load_model()


class ContentModel(BaseModel):
  content: str | list[str]


@app.post("/sentiment-analysis")
def sentiment_analysis_route(body: ContentModel):
  content = body.content
  result = sentiment.analysis(content)
  return {"sentiment": result}


if __name__ == "__main__":
  uvicorn.run(app, host="127.0.0.1", port=8000)