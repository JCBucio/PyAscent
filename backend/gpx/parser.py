import gpxpy
import numpy as np
from ..utils import haversine


def parse_gpx_text(gpx_text):
    """Parse GPX text and return a dict with points, lat/lon arrays, elevation and cumulative distance in meters.


    Returns:
    {
    'points': [(lat, lon, ele), ...],
    'lat': np.array([...]),
    'lon': np.array([...]),
    'ele': np.array([...]),
    'distance_m': np.array([...])
    }
    """
    gpx = gpxpy.parse(gpx_text)
    pts = []
    for track in gpx.tracks:
        for seg in track.segments:
            for p in seg.points:
                pts.append((p.latitude, p.longitude, p.elevation if p.elevation is not None else 0.0))
    if not pts:
        # fallback to waypoints
        for w in gpx.waypoints:
            pts.append((w.latitude, w.longitude, w.elevation if w.elevation else 0.0))
    if len(pts) < 2:
        raise ValueError("GPX path too short or missing points")


    dists = [0.0]
    for i in range(1, len(pts)):
        lat1, lon1, _ = pts[i - 1]
        lat2, lon2, _ = pts[i]
        dists.append(dists[-1] + haversine(lat1, lon1, lat2, lon2))

    lat = np.array([p[0] for p in pts])
    lon = np.array([p[1] for p in pts])
    ele = np.array([p[2] for p in pts])
    distance_m = np.array(dists)
    return {
        "points": pts,
        "lat": lat,
        "lon": lon,
        "ele": ele,
        "distance_m": distance_m
    }