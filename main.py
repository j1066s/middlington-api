from flask import Flask, jsonify
import requests
import feedparser
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "status": "Middlington API is running.",
        "endpoints": ["/full-data"]
    })

@app.route("/full-data", methods=["GET"])
def full_data():
    output = {}

    # --- ONS CPIH (Inflation) ---
    try:
        cpi_url = "https://api.beta.ons.gov.uk/v1/datasets/cpih01/editions/time-series/versions/4/observations"
        cpi_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "cpih1dim1G100000"
        }
        cpi_response = requests.get(cpi_url, params=cpi_params)
        cpi_data = cpi_response.json()
        output["inflation_rate"] = float(cpi_data["observations"][0]["observation"])
    except Exception as e:
        output["inflation_error"] = str(e)

    # --- ONS Unemployment Rate ---
    try:
        u_url = "https://api.beta.ons.gov.uk/v1/datasets/lms/editions/time-series/versions/3/observations"
        u_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "unem01"
        }
        u_response = requests.get(u_url, params=u_params)
        u_data = u_response.json()
        output["unemployment_rate"] = float(u_data["observations"][0]["observation"])
    except Exception as e:
        output["unemployment_error"] = str(e)

    # --- ONS Wage Growth (Earnings) ---
    try:
        wage_url = "https://api.beta.ons.gov.uk/v1/datasets/earn01/editions/time-series/versions/3/observations"
        wage_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "kac3"
        }
        wage_response = requests.get(wage_url, params=wage_params)
        wage_data = wage_response.json()
        output["real_wage_growth"] = float(wage_data["observations"][0]["observation"])
    except Exception as e:
        output["real_wage_error"] = str(e)

    # --- BBC News Headlines ---
    try:
        feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
        output["news_headlines"] = [
            {"title": entry.title, "link": entry.link}
            for entry in feed.entries[:5]
        ]
    except Exception as e:
        output["news_error"] = str(e)

    # --- Google Trends (UK) ---
    try:
        pytrends = TrendReq(hl="en-GB", tz=0, geo="GB")
        keywords = ["food prices", "Reform UK", "energy bills", "Tesco Clubcard"]
        pytrends.build_payload(keywords, cat=0, timeframe="now 7-d", geo="GB")
        interest = pytrends.interest_over_time()
        if not interest.empty:
            output["google_trends"] = {
                kw: int(interest[kw].iloc[-1]) for kw in keywords
            }
    except Exception as e:
        output["google_trends_error"] = str(e)

    # --- Weather from Open-Meteo ---
    try:
        weather = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.2&longitude=0.12&current_weather=true")
        output["weather"] = weather.json()["current_weather"]
    except Exception as e:
        output["weather_error"] = str(e)

    # --- Trussell Trust (Static Data) ---
    output["foodbank_usage_2024"] = {
        "households_helped": 3000000,
        "percent_with_children": 37,
        "main_reasons": [
            "Low income",
            "Benefit delays",
            "High energy bills"
        ],
        "source": "https://www.trusselltrust.org/news-and-blog/latest-stats/"
    }

    return jsonify(output)

# ✅ Required for deployment on Render or any cloud platform
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

