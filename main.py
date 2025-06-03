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

    # --- ONS CPIH (Inflation Rate) ---
    try:
        cpi_url = "https://api.beta.ons.gov.uk/v1/datasets/mm23/editions/time-series/versions/1/observations"
        cpi_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "L55O"
        }
        cpi_response = requests.get(cpi_url, params=cpi_params)
        if cpi_response.status_code == 200:
            cpi_data = cpi_response.json()
            obs = cpi_data.get("observations", [])
            if obs:
                output["inflation_rate"] = float(obs[0]["observation"])
            else:
                output["inflation_error"] = "No observations returned"
        else:
            output["inflation_error"] = f"ONS returned status {cpi_response.status_code}"
    except Exception as e:
        output["inflation_error"] = str(e)

    # --- ONS Unemployment Rate ---
    try:
        u_url = "https://api.beta.ons.gov.uk/v1/datasets/lms/editions/time-series/versions/1/observations"
        u_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "MGSX"
        }
        u_response = requests.get(u_url, params=u_params)
        if u_response.status_code == 200:
            u_data = u_response.json()
            obs = u_data.get("observations", [])
            if obs:
                output["unemployment_rate"] = float(obs[0]["observation"])
            else:
                output["unemployment_error"] = "No observations returned"
        else:
            output["unemployment_error"] = f"ONS returned status {u_response.status_code}"
    except Exception as e:
        output["unemployment_error"] = str(e)

    # --- ONS Wage Growth (Earnings) ---
    try:
        wage_url = "https://api.beta.ons.gov.uk/v1/datasets/lms/editions/time-series/versions/1/observations"
        wage_params = {
            "time": "latest",
            "geography": "K02000001",
            "aggregate": "KAC3"
        }
        wage_response = requests.get(wage_url, params=wage_params)
        if wage_response.status_code == 200:
            wage_data = wage_response.json()
            obs = wage_data.get("observations", [])
            if obs:
                output["real_wage_growth"] = float(obs[0]["observation"])
            else:
                output["real_wage_error"] = "No observations returned"
        else:
            output["real_wage_error"] = f"ONS returned status {wage_response.status_code}"
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

    # --- Weather (Open-Meteo) ---
    try:
        weather = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.2&longitude=0.12&current_weather=true")
        output["weather"] = weather.json().get("current_weather", {})
    except Exception as e:
        output["weather_error"] = str(e)

    # --- Trussell Trust Foodbank Stats (Static) ---
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

# ✅ Required for Render
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

