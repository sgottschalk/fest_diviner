import memcache
import requests
from diviner.utilities.Constants import cacheTtlSeconds


def getCacheKeyForRequest(url, params):
    """
    Generates a unique ascii string for the url and params, not necessarily a valid url.

    :param url: url piece
    :param params: parameters
    :return: unique string for this request
    """
    stringToHash = 'URL:' + url
    for key, value in params.iteritems():
        stringToHash += key + str(value)
    return stringToHash.encode('ascii', 'ignore')


def retrieveRequestJson(url, params):
    """
    Abstracts the response caching for a json request.

    :param url: base url
    :param params: query parameters
    :return: the response
    """
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    cacheKey = getCacheKeyForRequest(url, params)
    cachedValue = mc.get(cacheKey)
    if cachedValue is not None:
        return cachedValue
    else:
        response = requests.get(url, params=params)
        jsonResponse = response.json()
        mc.set(cacheKey, jsonResponse, cacheTtlSeconds)
        return jsonResponse