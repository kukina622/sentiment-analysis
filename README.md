# Sentiment Analysis

用於分析輸入的文字內容情緒。可以使用提供的 API 來進行分析。

## 環境設定

在執行此專案之前，請確保已安裝 pipenv。接著，使用以下指令來安裝專案所需的相依套件：

```bash
pipenv install
```
這將根據專案中的 Pipfile 安裝所有必要的相依套件。

## 模型
在開始使用情感分析 API 之前，請將訓練好的模型檔案放入 model 資料夾。

## API 使用方式

- **Endpoint**: `<host>/sentiment-analysis`
- **Method**: POST
- **Payload**: 接受兩種格式的輸入:
  - 單一句子輸入: `{"content": "這部電影真是太棒了，我非常喜歡它！"}`
  - 多句句子輸入: `{"content": ["這部電影真是太棒了，我非常喜歡它！", "真的很失望，浪費了我的時間。"]}`
- **回應內容**: 回應將以 JSON 格式提供，其中 `sentiment` 項目為情感分析的結果:
  - `{"sentiment": ["positive", "negative"]}`
