import requests
import json
import math
import random
from twilio.rest import Client
import html

COMPANY_NAME = "John Deere"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = " " #Your API KEY from News API
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key
}

news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
articles = news_response.json()["articles"][:3]
random_key = random.randint(0, len(articles) - 1)

news_titles = [articles[article]["title"] for article in range(len(articles))]
news_contents = [articles[article]["content"] for article in range(len(articles))]

stock_api_key = "YOUR API KEY" #Your API KEY from Alpha Vantage.
STOCK = "DE"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "apikey": stock_api_key,
    "interval": "60min",
    "datatype": "json",
    "to_symbol": "USD"
}
stock_response = requests.get(STOCK_ENDPOINT, stock_parameters)
stock_data = stock_response.json()

time_stamps = list((stock_data["Time Series (60min)"]).keys())
before_yesterday_closure_time = time_stamps[0]
yesterday_closure_time = time_stamps[16]
stock_before_yesterday_closing_value = float((stock_data["Time Series (60min)"][before_yesterday_closure_time]["4. close"]))
stock_yesterday_closing_value = float((stock_data["Time Series (60min)"][yesterday_closure_time]["4. close"]))

stock_percentage_difference = math.ceil(
        ((stock_before_yesterday_closing_value - stock_yesterday_closing_value) / stock_yesterday_closing_value) * 100)
direction = "🔻"
if (stock_before_yesterday_closing_value - stock_yesterday_closing_value) > 0:
      direction = "🔺"

account_sid = "  " # Your account sid from Twillio
auth_token = "  "  # Your authorization token from Twillio
client = Client(account_sid, auth_token)

content = (news_contents[random_key]).split("<ul>")
content = ".".join(content)
content = (content.split("."))
brief = html.unescape(content[0] + ".")
message_to_send = f"{STOCK}: {direction}{stock_percentage_difference}%\nHeadline: {news_titles[random_key]}\nBrief:{brief}" #This is the message to be sent.

message = client.messages \
    .create(
    body=message_to_send,
    from_='', # Your verified phone number from Twilio
    to=' ' # Your personal Phone Number
)
