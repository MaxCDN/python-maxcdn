from requests_oauthlib import OAuth1Session as OAuth1

# handle python 3.x
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse


class MaxCDN(object):
    def __init__(self, alias, key, secret, server="rws.maxcdn.com", **kwargs):
        self.url = "https://%s/%s" % (server, alias)
        self.client = OAuth1(key, client_secret=secret, **kwargs)

    def _get_headers(self, json=True):
        headers = {"User-Agent": "Python MaxCDN API Client"}
        if json:
            headers["Content-Type"] = "application/json"
        return headers

    def _get_url(self, end_point):
        if not end_point.startswith("/"):
            return "%s/%s" % (self.url, end_point)
        else:
            return self.url + end_point

    def _parse_json(self, response):
        try:
            return response.json()
        except ValueError, e:
            raise ValueError(e.message + ". Raw response was:\n\n"
                             + response._content)

    def _data_request(self, method, end_point, data, **kwargs):
        if data is None and "params" in kwargs:
            params = kwargs.pop("params")
            if type(params) is str:
                params = urlparse.parse_qs(params)
            data = params
        action = getattr(self.client, method)
        response = action(self._get_url(end_point), data=data,
                          headers=self._get_headers(json=True), **kwargs)
        return self._parse_json(response)

    def get(self, end_point, data=None, **kwargs):
        return self._data_request("post", end_point, data=data, **kwargs)

    def patch(self, end_point, data=None, **kwargs):
        return self._data_request("post", end_point, data=data, **kwargs)

    def post(self, end_point, data=None, **kwargs):
        return self._data_request("post", end_point, data=data, **kwargs)

    def put(self, end_point, data=None, **kwargs):
        return self._data_request("put", end_point, data=data, **kwargs)

    def delete(self, end_point, data=None, **kwargs):
        return self._data_request("delete", end_point, data=data, **kwargs)

    def purge(self, zoneid, file_or_files=None, **kwargs):
        path = "/zones/pull.json/%s/cache" % (zoneid)
        if file_or_files is not None:
            return self.delete(path, data={"files": file_or_files}, **kwargs)
        return self.delete(path, **kwargs)
