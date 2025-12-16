import json
import time
from shapely.geometry import LineString
import polyline
from ..db import get_conn
from ..utils import meters_to_deg_lat, meters_to_deg_lon, haversine
from .client import strava_get


def _polyline_to_linestring(seg_json):
    mp = seg_json.get("map", {})
    pts = None
    if mp.get("polyline"):
        pts = polyline.decode(mp.get("polyline"))
    elif seg_json.get("summary_polyline"):
        pts = polyline.decode(seg_json.get("summary_polyline"))
    if pts:
        coords = [(lon, lat) for lat, lon in pts]
        return LineString(coords)
    # fallback
    s = seg_json.get("start_latlng") or [None, None]
    e = seg_json.get("end_latlng") or [None, None]
    if s[0] is None or e[0] is None:
        return LineString([])
    return LineString([(s[1], s[0]), (e[1], e[0])])


def cache_lookup(seg_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT json FROM segments WHERE id=?", (seg_id,))
    row = cur.fetchone()
    if row:
        return json.loads(row[0])
    return None


def cache_store(seg_id, data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO segments (id, json, last_fetch) VALUES (?, ?, ?)",
    (seg_id, json.dumps(data), int(time.time())))
    conn.commit()


def explore_segments_at_point(lat, lon, access_token, radius_m=150):
    lat_d = meters_to_deg_lat(radius_m)
    lon_d = meters_to_deg_lon(radius_m, lat)
    lat1, lon1 = lat - lat_d, lon - lon_d
    lat2, lon2 = lat + lat_d, lon + lon_d
    bounds = f"{lat1},{lon1},{lat2},{lon2}"
    params = {"bounds": bounds, "activity_type": "riding"}
    data = strava_get("/segments/explore", access_token, params=params)
    return data.get("segments", [])


def fetch_segment_by_id(seg_id, access_token):
    cached = cache_lookup(seg_id)
    if cached:
        return cached
    data = strava_get(f"/segments/{seg_id}", access_token)
    cache_store(seg_id, data)
    return data


def match_segment_to_gpx(seg_json, gpx_linestring, tolerance_m=30):
    seg_ls = _polyline_to_linestring(seg_json)
    if seg_ls.is_empty or gpx_linestring.is_empty:
        return 0.0
    # approximate tolerance in degrees at mid-lat
    mid_lat = (gpx_linestring.bounds[1] + gpx_linestring.bounds[3]) / 2.0 if gpx_linestring.bounds else 0.0
    tol_deg = meters_to_deg_lat(tolerance_m)
    buffered = gpx_linestring.buffer(tol_deg)
    inter = seg_ls.intersection(buffered)
    if inter.is_empty:
        return 0.0


    def geom_length_m(geom):
        if geom.is_empty:
            return 0.0
        if geom.geom_type == 'LineString':
            coords = [(lat, lon) for lon, lat in geom.coords]
            s = 0.0
            for i in range(1, len(coords)):
                s += haversine(coords[i-1][0], coords[i-1][1], coords[i][0], coords[i][1])
            return s
        elif geom.geom_type == 'MultiLineString':
            s = 0.0
            for part in geom:
                s += geom_length_m(part)
            return s
        else:
            return 0.0


    overlap_len = geom_length_m(inter)
    seg_len = geom_length_m(seg_ls)
    if seg_len <= 0:
        return 0.0
    return overlap_len / seg_len


def segment_linestring(seg_json):
    return _polyline_to_linestring(seg_json)