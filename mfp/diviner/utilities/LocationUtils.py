from math import sin, radians, cos, atan, sqrt


def haversine(lat1, lng1, lat2, lng2):
    """
    Computes the distance between 2 points on a map.

    :param lat1:
    :param lng1:
    :param lat2:
    :param lng2:
    :return:
    """
    radius = 6371
    diffLat = radians(lat2 - lat1)
    diffLong = radians(lng2 - lng1)
    lat1Rad = radians(lat1)
    lat2Rad = radians(lat2)
    formulaA = sin(diffLat / 2)**2 + sin(diffLong / 2)**2 * cos(lat1Rad) * cos(lat2Rad)
    formulaC = 2 * atan(sqrt(formulaA))
    return formulaC * radius