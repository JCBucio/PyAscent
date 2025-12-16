import time
import requests
from urllib.parse import urlencode
from ..config import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_REDIRECT_URI, STRAVA_API_BASE, PAUSE_BETWEEN_CALLS


def authorize_url():
    params = {
        "client_id": STRAVA_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": STRAVA_REDIRECT_URI,
        "approval_prompt": "auto",
        "scope": "read"
    }
    return f"https://www.strava.com/oauth/authorize?{urlencode(params)}"


def exchange_token(code):
    url = "https://www.strava.com/oauth/token"
    resp = requests.post(url, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })
    resp.raise_for_status()
    return resp.json()


def refresh_token(refresh_token):
    url = "https://www.strava.com/oauth/token"
    resp = requests.post(url, data={
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })
    resp.raise_for_status()
    return resp.json()


def strava_get(path, access_token, params=None):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{STRAVA_API_BASE}{path}"
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 429:
        reset = int(r.headers.get("Retry-After", "30"))
        time.sleep(reset)
        r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    time.sleep(PAUSE_BETWEEN_CALLS)
    return r.json()