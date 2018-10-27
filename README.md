# 正體中文在地化譯文資料庫
## 取得譯文
### 透過 `glossary.py` 取得某字彙譯文
1. 下載 Python 3。GNU/Linux 大部份發行版應該已預設安裝，若無
   或是使用 macOS / Windows，前往 [Python 
官方](http://www.python.org)下載。

2. 使用以下指令取得譯文：
   `python3 glossary.py match "原文"`：尋找與 原文 完全相符的字彙
   `python3 glossary.py search "原文"`：尋找包含 原文 的字彙譯文

### 解析 JSON
`glossary.json` 字彙檔案為 JSON 格式，其形式如下：

```
原文: 譯文
```

若您打算用於您的程式，只需要解析 `glossary.json` 即可。

## 更新譯文
### 手動修改 JSON 檔案 (不推薦！)
開啟 `glossary.json` 並遵循《取得譯文》一節的《解析 JSON》部份的格式。

### 使用 `glossary.py`
輸入 `python3 glossary.py` 檢視關於更新譯文的資訊。

## 作者
```
pan93412 <http://www.github.com/pan93412>, 2018.
```
