import requests
import os
from twilio.rest import Client

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Environment variables for News API
news_api = os.environ.get("news_apikey")

# Environment variables for Alpha Vantage
av_apikey = os.environ.get("av_apikey")

# Environment variables for Twilio REST API
twilio_acc = os.environ.get("twilio_acc")
twilio_auth = os.environ.get("twilio_auth")
twilio_num = os.environ.get("twilio_num")
my_num = os.environ.get("my_num")


# Get stock data
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": av_apikey
}
data = requests.get(url="https://www.alphavantage.co/query", params=STOCK_PARAMS)
data.raise_for_status()

data_list = [value for (key, value) in data.json()["Time Series (Daily)"].items()]
recent = float(data_list[0]["4. close"])
previous = float(data_list[1]["4. close"])
date = data.json()["Meta Data"]["3. Last Refreshed"]
delta = (recent - previous) / recent * 100


# Get news on company
NEWS_PARAMS = {
    "apikey": news_api,
    "q": COMPANY_NAME
}

news = requests.get(url="https://newsapi.org/v2/top-headlines", params=NEWS_PARAMS).json()['articles']
descriptions = []
for i in range(len(news)):
    if len(descriptions) == 3:
        break
    else:
        descriptions.append(news[i]['title'])
        descriptions.append(news[i]['description'])


# Format increase/decrease in percentage for output message
def pct(x):
    if x >= 0:
        return f"🔺{x}%"
    else:
        return f"🔻{x}%"


msg = f"\n{STOCK}: {pct(round(delta, 2))}\nDate: {date}"
for i in range(0, len(descriptions), 2):
    msg += f"\nHeadline: {descriptions[i]}\nBrief: {descriptions[i + 1]}"

# Send message
client = Client(twilio_acc, twilio_auth)
message = client.messages.create(
    body=msg,
    from_=twilio_num,
    to=my_num
)

# PLEASE READ

"""
Environment variables required:
av_apikey
news_api
twilio_acc
twilio_auth
twilio_num
my_num
"""
