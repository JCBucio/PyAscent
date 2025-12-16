import math


# Haversine distance in meters
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1); dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))



def meters_to_deg_lat(m):
    return m / 111111.0




def meters_to_deg_lon(m, lat):
    return m / (111111.0 * math.cos(math.radians(lat)) + 1e-12)