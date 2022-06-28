import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime,timedelta

#get the data
info = []
for i in range(1, 3):
    url = f"https://www.taitung.gov.tw/News.aspx?n=13370&page={i}"
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "lxml")
        trs = soup.find("tbody").find_all("tr")
        #get publish_date, title, article_url. And add to info list in dict form.
        for tr in trs:
            publish_date = tr.find("td", attrs={"data-title": "發布日期"}).text    
            title = tr.find("td", attrs={"data-title": "新聞標題"}).span.a["title"]
            article_url = tr.find("td", attrs={"data-title": "新聞標題"}).span.a["href"]
            info.append(
                {"date": publish_date,
                 "title":title,
                 "article_url":"https://www.taitung.gov.tw/" + article_url                
                        }
            )
        #transter to dataframe
        df_info = pd.DataFrame(info)


#create date format
yesterday = datetime.now() - timedelta(days=1)
date_year_month_day = str(yesterday.year - 1911) + "-" + yesterday.strftime("%m-%d")

#filter DataFrame by datetime
df_specific_day = df_info[df_info["date"] >= date_year_month_day]

txt_string = df_specific_day[["title", "article_url"]].values

raw_txt = "\n"  + "昨天及今天的臺東縣政新聞:" + "\n"
for index, value in enumerate(txt_string):
    raw_txt += f"{index+1}:{value[0]}\n,{value[1]}\n"

def Line_Notify(token, message):
    headers = {"Authorization": "Bearer " + token}
    param = {'message': message}   
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = param)
    return r.status_code

token = 'BfShFs8u34oFjOKqmFMlr2aNi9lyMYxdNNQuBwOpTxH'
result = Line_Notify(token, raw_txt)
print(result) # 印一下回傳代碼
print("ok")

