import os
import io
from fastapi import FastAPI, Request, UploadFile, Form, Depends
from fastapi.responses import RedirectResponse, StreamingResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from .config import SECRET_KEY, STRAVA_REDIRECT_URI
from .gpx.parser import parse_gpx_text
from .gpx.sampling import sample_indices_along_distance
from .strava.client import authorize_url, exchange_token
# In here i will import the functions of strava/segments.py and plotting/profile_plotter.py
#from .strava.segments import explore_segments_at_point, fetch_segment_by_id, match_segment_to_gpx, segment_linestring
#from .plotting.profile_plotter import plot_profile_and_segments
from .utils import meters_to_deg_lat
from shapely.geometry import LineString
from .config import SAMPLE_INTERVAL_M, EXPLORE_RADIUS_M, OVERLAP_THRESHOLD


app = FastAPI(title="PyAscent Backend")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


HTML_INDEX = """
<html>
    <head><title>PyAscent Backend</title></head>
    <body>
        <h1>PyAscent Backend</h1>
        <p><a href="/strava/login">Connect with Strava</a></p>
        <form action="/upload_gpx" enctype="multipart/form-data" method="post">
            <p><input name="gpxfile" type="file"/> <input type="submit" value="Upload GPX"/></p>
        </form>
        <p>After connecting to Strava, upload a GPX and the server will query Strava segments and return a profile PNG.</p>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return HTML_INDEX


@app.get("/strava/login")
def strava_login():
    return RedirectResponse(authorize_url())


@app.get("/strava/callback")
async def strava_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "no code returned"}, status_code=400)
    token_json = exchange_token(code)
    # store access token in session
    request.session["strava_token"] = token_json.get("access_token")
    request.session["strava_refresh"] = token_json.get("refresh_token")
    request.session["strava_expires_at"] = token_json.get("expires_at")
    return RedirectResponse("/")