import pandas as pd
import requests
from datetime import datetime,timedelta

#get the data
df = pd.DataFrame()
for i in range(1, 3):
    url = f"https://www.taitung.gov.tw/News.aspx?n=13370&page={i}"
    df = pd.concat([df, pd.read_html(url)[0]], ignore_index=True)

#create date format
yesterday = datetime.now() - timedelta(days=1)
date_year_month_day = str(yesterday.year - 1911) + "-" + yesterday.strftime("%m-%d")

#filter DataFrame
df_specific_day = df[df["發布日期"] >= date_year_month_day]

txt_string = df_specific_day["新聞標題"].values
raw_txt = "\n"  + "昨天及今天的臺東縣政新聞:" + "\n"
for i, string in zip(list(range(1,len(txt_string)+1)), txt_string):
    raw_txt += f"{i}:{string}\n"

#send message to line
def Line_Notify(token, message):
    headers = {"Authorization": "Bearer " + token}
    param = {'message': message}   
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = param)
    return r.status_code

token = 'BfShFs8u34oFjOKqmFMlr2aNi9lyMYxdNNQuBwOpTxH'
result = Line_Notify(token, raw_txt)
print(result) # 印一下回傳代碼
print("ok")