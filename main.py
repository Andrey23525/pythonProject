import json
from random import choice
from requests import get
import pandas, time, random
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlopen

def wait(start, end):
    random.seed(time.time())
    time.sleep(random.randint(start, end))

tables = []
indexs = [int(n) for n in range(1, 34)]

for j in range(1, 34):
    ts = time.time()
    i = choice(indexs)
    indexs.remove(i)

    try:
        downloadUrl = ""
        wait(1, 10)
        with urlopen("https://urfu.ru/api/ratings/info/27/" + str(i) + "/") as url:
            downloadUrl = "https://urfu.ru" + json.loads(url.read().decode())["url"]
    except HTTPError:
        continue

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}

        html = get(downloadUrl, headers=headers).text.encode("iso-8859-1").decode("UTF-8")

        if len(html) > 1:
            t = pandas.read_html(html, attrs={"class": "alpha supp table-header"})
            tables.append(t[0])
    except ValueError:
        continue
    print(f"[{datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}]", str(round((1 - len(indexs)/33)*100)), '%')
res = pandas.concat(tables).drop_duplicates().reset_index(drop=True)
res.to_csv("res.csv")
# res.to_csv("../postPythonProject/res.csv")
print("OK")