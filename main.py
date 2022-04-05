import requests
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Stock_API_KEY="2KCK99HVB83HMTJ6"
Stock_API_KEY=os.environ['STOCK_API_KEY']
news_api_key=os.environ['news_api_key']
twilio_SID=os.environ['TWILIO_SID']
twilio_auth_tocken=os.environ['TWILIO_AUTH']

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey":Stock_API_KEY
}

stock_responce=requests.get(url=STOCK_ENDPOINT,params=stock_params)
data=stock_responce.json()["Time Series (Daily)"]


data_list=[value for (key,value) in data.items()]

#to get yesterday closing price
yesterday_closing_data=data_list[0]["4. close"]
print(yesterday_closing_data)

#day before yesterday closing price
day_before_yesterday_closing_price=data_list[1]["4. close"]
print(day_before_yesterday_closing_price)

#differnce of last two days
difference=abs(float(yesterday_closing_data)-float(day_before_yesterday_closing_price))


up_down=None
if difference>0:
    up_down="🔺"
else:
    up_down="🔻"



diff_percent=round((difference/float(yesterday_closing_data))*100)


if abs(diff_percent)>5:
    print("getnews")
    news_params={
    "q":STOCK,
    "qlnTitle":COMPANY_NAME,
    "apiKey":news_api_key,

    }
    news_responce=requests.get(url=NEWS_ENDPOINT,params=news_params)
    article=news_responce.json()["articles"]
    three_article=article[:3]

    formatted_article=[f"{STOCK}:{up_down}{diff_percent}%\nHeadLine:{article['title']}. \nBrief:{article['description']}" for article in three_article]


    #sending msg to the client
    client=Client(twilio_SID,twilio_auth_tocken)
    for article in formatted_article:
        message=client.messages.create(
            body=article,
            from_="###########",#twilio number
            to="#######"    #client number with contry code
        )
