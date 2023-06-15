import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API = ""  # enter stock api
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = ""   # enter news api
TWILIO_AUTH_TOKEN = ""  # enter twilio auth token
TWILIO_SID = ""  # enter twilio sid

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "datatype": 'json',
    "apikey": STOCK_API
}

news_params = {
    "apiKey": NEWS_API,
    "qInTitle": COMPANY_NAME,
}

# Get yesterday's closing stock price
response = requests.get(STOCK_ENDPOINT, params=stock_params)
print(response.raise_for_status())
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = float(data_list[0]['4. close'])

# Get the day before closing stock price
day_before_yesterday_price = float(data_list[1]['4. close'])

# Get the difference between the two closing days
difference = (yesterday_closing_price - day_before_yesterday_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Find the percentage of how much the stock increased or decreased
avg = ((yesterday_closing_price + day_before_yesterday_price) / 2)
percentage_difference = abs(round((difference / avg) * 100))

# If the percentage change is equal to or greater than 5% notify by text message
if abs(percentage_difference) >= 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]  # Get three articles using slicing

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {articles['title']}. \nBrief:"
                          f"{articles['description']}" for articles in three_articles]

# Send each message as a separate message using twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for articles in formatted_articles:
        message = client.messages.create(
            body=articles,
            from_="+",  # enter twilio phone number
            to="+"  # enter your phone number
        )


