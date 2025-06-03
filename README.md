# Middlington API

A Flask-based REST API providing various UK data feeds including weather, news, ONS statistics, and polling data.

## Features

- **Weather**: Current weather data for Middlington
- **News**: Latest BBC news headlines via RSS feed
- **ONS Data**: UK economic statistics including GDP, inflation, unemployment, house prices, population, and retail sales
- **Political Polling**: YouGov-style polling data
- **TikTok Trends**: Current trending topics

## API Endpoints

- `GET /` - API status
- `GET /weather` - Weather information
- `GET /news-headlines` - Latest BBC news
- `GET /tiktok-trends` - Trending topics
- `GET /ons-gdp` - UK GDP data
- `GET /ons-inflation` - UK inflation rates
- `GET /ons-unemployment` - UK unemployment rates
- `GET /ons-house-prices` - UK house prices
- `GET /ons-population` - UK population data
- `GET /ons-retail-sales` - UK retail sales data
- `GET /yougov-polls` - Political polling data

## Installation

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run the API: `python main.py`

The API will be available at `http://localhost:5000`

## Deployment

This project is ready to deploy on Replit or any Python hosting platform.

## Dependencies

- Flask - Web framework
- feedparser - RSS feed parsing
- requests - HTTP requests for ONS API
