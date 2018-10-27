'''正體中文在地化譯文資料庫: 輸入 glossary.py'''
# 匯入元件
import os, shutil, json, sys
from urllib import request

# 定義變數
GITURL = "https://github.com/l10n-tw/zh_glossary/"
GITRAWURL = "https://raw.githubusercontent.com/l10n-tw/zh_glossary/master/"
VER = "v0.1.1-beta"

usage = '''[正體中文在地化譯文資料庫]
版本：{2}

用法：python3 {0} [功能] [引數]
 
 [說明]
   1. 引數建議都加上 ""
      ex. "pattern"、
          "pattern" "樣式"。
 [功能]
   - 查詢類別 - 
   search:
     遞迴搜尋資料庫，找到與搜尋字串類似的詞彙
     [引數] = "[搜尋字串]"
     範例：search "pattern" -- 尋找與 pattern 類似的原文譯文
     
   match:
     找到與搜尋字串完全相符的詞彙，搜尋速度較快。
     [引數] = "[搜尋字串]"
     範例：match "pattern" -- 尋找與 pattern 相同的原文譯文
     
   - 編輯類別 -
   edit:
     增加或編輯字彙。
     [引數] = "[原文]" "[譯文]"
     範例：edit "pattern" "樣式;胚騰" -- 將 pattern 的譯文設定為 樣式;胚騰
     
   remove:
     移除 [原文] 字彙。
     [引數] = "[原文]"
     範例：remove "pattern" -- 移除 pattern 的譯文
    
'''.format(sys.argv[0], GITURL+"issues", VER)

def query(glos, orig):
  """
  用於 search() 和 match() 的查詢函式，
  回傳格式化過的結果。
  """
  return "原文：{0}  譯文：{1}".format(orig, glos[orig])

def search(glos, pattern):
  """
  搜尋類似 pattern 的字彙
  
  glos (dict) 讀入的字彙表資料
  pattern (str) 搜尋樣式
  """
  for i in glos:
    if i.find(pattern) != -1:
      print(query(glos, i))
  return
      
def match(glos, pattern):
  """
  搜尋完全相符 pattern 的字彙
  
  glos (dict) 讀入的字彙表資料
  pattern (str) 搜尋樣式
  """
  if pattern not in glos:
    print("此資料庫沒有「{}」字彙".format(pattern))
  else:
    print(query(glos, pattern))
  return

def edit(glos, orig, tran):
  '''
  增加或編輯 orig 字彙的翻譯。
  
  glos (dict) glossary.json 讀出的 Dict 型態資料
  orig (str) 原文
  tran (str) 譯文 (; 分割)
  
  回傳：修改過的 glos
  '''
  
  temp = {orig: tran}
  glos.update(temp)
  print("順利修改：現在 {0} 的資料已經是 {1}。".format(orig, tran))
  return glos

def remove(glos, orig):
  '''
  移除 original 字彙的翻譯
  
  glos (dict) glossary.json 讀出的 Dict 型態資料
  orig (str) 原文
  
  回傳：修改過的 glos
  '''
  if glos.get(orig, None) != None:
    glos.pop(orig)
    print("順利移除：成功刪除 {0} 的譯文資料。".format(orig))
  else:
    print("移除失敗：沒有 {0} 字彙。".format(orig))
    
  return glos

def push():
  '''透過 git 推送翻譯到 master 分支。需要 git!'''
  print("開始推送程序。稍候可能需要輸入帳號與密碼。")
  if os.path.exists("GLOTMP"):
    shutil.rmtree("GLOTMP")
  os.system("git clone --depth 1 {} GLOTMP".format(GITURL)) # Clone GITURL 到 GLOTMP
  
  if os.path.exists("GLOTMP") == False:
    print("錯誤：Clone 失敗")

  os.remove("./GLOTMP/glossary.json") # 移除 GLOTMP 原有的 glossary.json 檔案
  shutil.copy("glossary.json", "GLOTMP") # 複製此處的 glossary.json 到 GLOTMP
  os.chdir("GLOTMP") # 切換工作目錄到 GLOTMP
  os.system('git commit -am "[CG] Update Glossary File."') # 提交 commit
  os.system('git push')  # 推送變更。此處需要使用者驗證
  os.chdir("..") # 工作目錄復位
  shutil.rmtree("GLOTMP") # 刪除已使用完畢的 GLOTMP
  print("推送程序完成。")
  return

def fetch():
  '''發出 HTTP 請求，來下載最新的 glossary.json 檔案'''
  print("正在抓取最新的 glossary.json 檔案…", end="")
  theRequest = request.Request(GITRAWURL + "glossary.json")
  theResponse = request.urlopen(theRequest)
  dataRaw = theResponse.read()
  f = open("glossary.json", "w", encoding="UTF-8")
  f.write(dataRaw.decode("UTF-8"))
  f.flush()
  f.close(); theResponse.close()
  print("抓取成功。")
  exit()
  return

def main():
  # 如果有 glossary.json 則讀出 gloassary.json 中資料
  # 如果沒有，或是 glossary.json 是空的，則將變數設定為 {} (空 dict)
  if os.path.isfile("glossary.json"):
    file = open("glossary.json", "r")
    glos = file.read()
    if glos != "" and glos != "{}":
      glos = json.loads(glos)
    else:
      glos = {}
    file.close()
  else:
    glos = {}
  
  # 建立 glossary_new.json
  file = open("glossary_new.json", "w+")
  if len(sys.argv) < 2:
    print(usage) # 說明文字
  else:
    if sys.argv[1] == "search" and len(sys.argv) == 3:
      # sys.argv[2] 預期為 樣式
      search(glos, sys.argv[2])
    elif sys.argv[1] == "match" and len(sys.argv) == 3:
      # sys.argv[2] 預期為 樣式
      match(glos, sys.argv[2])
    elif sys.argv[1] == "edit" and len(sys.argv) == 4:
      # sys.argv[2] 預期為 原文
      # sys.argv[3] 預期為 譯文
      glos = edit(glos, sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "remove" and len(sys.argv) == 3:
      # sys.argv[2] 預期為 原文
      glos = remove(glos, sys.argv[2])
    elif sys.argv[1] == "push":
      push()
    elif sys.argv[1] == "fetch":
      fetch()
    else:
      print(usage)
    
  jsonData = json.dumps(glos, ensure_ascii=False, indent=2)
  file.write(jsonData)
  file.flush()
  file.close()
  
  if os.path.exists("glossary.json"): os.remove("glossary.json")
  os.rename("glossary_new.json", "glossary.json")
  
if __name__ == "__main__":
  main()
else:
  print("雖然這軟體是模組化的，但也別把它當模組用 QQ")


