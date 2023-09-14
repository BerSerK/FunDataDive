import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = "http://www.qzjy114.com/nd.jsp?id=388"
response = requests.get(url, headers=headers)

data = pd.read_html(response.text)
print(data[0])
df = data[0]
df.to_csv('zhongxue.csv', index=False, header=False)