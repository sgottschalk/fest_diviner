import json
import urllib
from django.core.cache import cache
import httplib2
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
        stringToHash += key + urllib.quote_plus(str(value))
    return stringToHash.encode('ascii', 'ignore')


def retrieveRequestJson(url, params):
    """
    Abstracts the response caching for a json request.

    :param url: base url
    :param params: query parameters
    :return: the response
    """
    cacheKey = getCacheKeyForRequest(url, params)
    cachedValue = cache.get(cacheKey)
    if cachedValue is not None:
        return cachedValue
    else:
        h = httplib2.Http()
        urlWithParams = url + "?" + urllib.urlencode(params)
        resp, content = h.request(urlWithParams, "GET")
        jsonResponse = json.loads(content)
        cache.set(cacheKey, jsonResponse, cacheTtlSeconds)
        return jsonResponse