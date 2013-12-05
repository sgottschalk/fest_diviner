from math import sin, radians, cos, atan, sqrt


def haversine(lat1, lng1, lat2, lng2):
    radius = 6371
    diffLat = radians(lat2 - lat1)
    diffLong = radians(lng2 - lng1)
    lat1Rad = radians(lat1)
    lat2Rad = radians(lat2)
    formulaA = sin(diffLat / 2)**2 + sin(diffLong / 2)**2 * cos(lat1Rad) * cos(lat2Rad)
    formulaC = 2 * atan(sqrt(formulaA))
    return formulaC * radius

# messing around
# distance from SLC to Vancouver BC
# distance = haversine(40.7637962, -111.876534, 49.299564, -123.13395)
# print distance
#
# addedDistance = haversine(40.7637962, -111.876534, 47.0959, -119.983) + haversine(47.0959, -119.983, 49.299564, -123.13395)
#
# print addedDistance - distance