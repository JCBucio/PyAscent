import os
from dotenv import load_dotenv


load_dotenv()


# Strava app credentials
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost:8000/strava/callback")


# App settings
SECRET_KEY = os.getenv("APP_SECRET_KEY", "super-secret-change-me")
CACHE_DB = os.getenv("CACHE_DB", "./pyascent_cache.sqlite")


# Strava API base
STRAVA_API_BASE = "https://www.strava.com/api/v3"


# behavior tunables
SAMPLE_INTERVAL_M = int(os.getenv("SAMPLE_INTERVAL_M", "500"))
EXPLORE_RADIUS_M = int(os.getenv("EXPLORE_RADIUS_M", "150"))
OVERLAP_THRESHOLD = float(os.getenv("OVERLAP_THRESHOLD", "0.6"))
PAUSE_BETWEEN_CALLS = float(os.getenv("PAUSE_BETWEEN_CALLS", "0.25"))