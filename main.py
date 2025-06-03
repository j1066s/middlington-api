from flask import Flask, jsonify
import feedparser
import requests

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def get_weather():
    return jsonify({
        "location": "Middlington",
        "forecast": "Rainy",
        "temperature_c": 13,
        "wind_speed_kph": 22,
        "warning": "Yellow weather warning for localised flooding"
    })

@app.route("/tiktok-trends", methods=["GET"])
def get_tiktok_trends():
    return jsonify({
        "tiktok_trends": [
            "Air fryer pasta recipes",
            "Skip meals to save money challenge",
            "POV: Budget Mum UK",
            "Corner shop hauls",
            "Quiet quitting remix"
        ]
    })

@app.route("/news-headlines", methods=["GET"])
def get_news_headlines():
    feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(feed_url)
    headlines = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]
    return jsonify({"headlines": headlines})

@app.route("/ons-gdp", methods=["GET"])
def get_ons_gdp():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/IHYQ/dataset/UKEA/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-5:]
            
            ons_data = []
            for obs in observations:
                ons_data.append({
                    "value": obs.get('value', 'N/A'),
                    "date": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK GDP Quarterly Data",
                "description": "Gross Domestic Product: chained volume measures: Seasonally adjusted £m",
                "latest_data": ons_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS GDP data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS GDP data", "message": str(e)}), 500

@app.route("/ons-inflation", methods=["GET"])
def get_ons_inflation():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/D7G7/dataset/MM23/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-12:]
            
            inflation_data = []
            for obs in observations:
                inflation_data.append({
                    "rate_percent": obs.get('value', 'N/A'),
                    "date": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK Inflation Rate",
                "description": "Consumer Prices Index including owner occupiers' housing costs (CPIH) 12-month rate",
                "latest_data": inflation_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS inflation data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS inflation data", "message": str(e)}), 500

@app.route("/ons-unemployment", methods=["GET"])
def get_ons_unemployment():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/MGSX/dataset/LMS/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-12:]
            
            unemployment_data = []
            for obs in observations:
                unemployment_data.append({
                    "rate_percent": obs.get('value', 'N/A'),
                    "date": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK Unemployment Rate",
                "description": "Unemployment rate (aged 16 and over, seasonally adjusted)",
                "latest_data": unemployment_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS unemployment data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS unemployment data", "message": str(e)}), 500

@app.route("/ons-house-prices", methods=["GET"])
def get_ons_house_prices():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/WLPE/dataset/HPSSA/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-12:]
            
            house_price_data = []
            for obs in observations:
                house_price_data.append({
                    "average_price_gbp": obs.get('value', 'N/A'),
                    "date": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK House Prices",
                "description": "Average house prices for the United Kingdom (seasonally adjusted)",
                "latest_data": house_price_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS house price data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS house price data", "message": str(e)}), 500

@app.route("/ons-population", methods=["GET"])
def get_ons_population():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/UKPOP/dataset/POP/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-5:]
            
            population_data = []
            for obs in observations:
                population_data.append({
                    "population_thousands": obs.get('value', 'N/A'),
                    "year": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK Population",
                "description": "UK population estimates (mid-year, thousands)",
                "latest_data": population_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS population data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS population data", "message": str(e)}), 500

@app.route("/ons-retail-sales", methods=["GET"])
def get_ons_retail_sales():
    try:
        ons_url = "https://api.ons.gov.uk/timeseries/J5EH/dataset/DRSI/data"
        response = requests.get(ons_url)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])[-12:]
            
            retail_data = []
            for obs in observations:
                retail_data.append({
                    "index_value": obs.get('value', 'N/A'),
                    "date": obs.get('date', 'N/A')
                })
            
            return jsonify({
                "data_source": "ONS UK Retail Sales",
                "description": "Retail sales quantity (seasonally adjusted)",
                "latest_data": retail_data
            })
        else:
            return jsonify({"error": "Failed to fetch ONS retail sales data"}), 500
    
    except Exception as e:
        return jsonify({"error": "Error fetching ONS retail sales data", "message": str(e)}), 500

@app.route("/yougov-polls", methods=["GET"])
def get_yougov_polls():
    return jsonify({
        "data_source": "YouGov UK Political Polling",
        "description": "Latest UK voting intention polls",
        "polls": [
            {
                "party": "Conservative",
                "percentage": 24,
                "change": "-2"
            },
            {
                "party": "Labour", 
                "percentage": 42,
                "change": "+1"
            },
            {
                "party": "Liberal Democrat",
                "percentage": 12,
                "change": "0"
            },
            {
                "party": "Reform UK",
                "percentage": 15,
                "change": "+1"
            },
            {
                "party": "Green",
                "percentage": 6,
                "change": "0"
            }
        ],
        "poll_date": "2024-01-15",
        "sample_size": 1742,
        "note": "This is sample data - YouGov doesn't provide a free public API"
    })

@app.route("/")
def index():
    return jsonify({"status": "Middlington API is running."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
