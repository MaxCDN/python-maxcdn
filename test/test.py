import mock
import unittest
import requests
from maxcdn import MaxCDN

################################################################################
# Mock as needed.
def mock_request(method, url, *args, **kwargs):
    pass

class Response(object):
    def __init__(self, method, code=200, data={"foo":"bar"}):
        self._json = { "code": code, "method": method, "data": data }

    def json(self):
        return self._json

class ErrorResponse(object):
    def __init__(self, code=200, badcontent="Some bad content."):
        self._content = badcontent

    def json(self):
        raise ValueError("No JSON object could be decoded")

def response(method, **kwargs):
    return Response(method, **kwargs)

def error_response(**kwargs):
    return ErrorResponse(**kwargs)

#
################################################################################

class MaxCDNTests(unittest.TestCase):

    def setUp(self):
        self.alias  = "test_alias"
        self.key    = "test_key"
        self.secret = "test_secret"
        self.server = "rws.example.com"
        self.maxcdn = MaxCDN(self.alias, self.key, self.secret, server=self.server)

    def test_init(self):
        self.assertTrue(self.maxcdn)
        self.assertEqual(self.maxcdn.url, "https://rws.example.com/test_alias")

    def test_get_url(self):
        self.assertEqual(self.maxcdn._get_url("/foo.json"),
                "https://rws.example.com/test_alias/foo.json")

        self.assertEqual(self.maxcdn._get_url("foo.json"),
                "https://rws.example.com/test_alias/foo.json")

    def test_data_request(self):
        for meth in [ "post", "put", "delete" ]:
            requests.Session.request = mock.create_autospec(mock_request,
                    return_value=response(meth))
            self.assertEqual(self.maxcdn._data_request(meth, meth+".json",
                data={"foo":"bar"}), { "code": 200, "method": meth, "data": { "foo":"bar" } })

            requests.Session.request = mock.create_autospec(mock_request,
                    return_value=error_response())
            with self.assertRaises(ValueError):
                self.maxcdn._data_request(meth, meth+".json", data={"foo":"bar"})

    def test_get(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("get"))
        self.assertEqual(self.maxcdn.get("/get.json"),
                { "code": 200, "method": "get", "data": { "foo":"bar" } })

        requests.Session.request = mock.create_autospec(mock_request,
                return_value=error_response())
        with self.assertRaises(ValueError):
            self.maxcdn.get("/get.json")

    def test_post(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("post"))
        self.assertEqual(self.maxcdn.post("/post.json", data={ "foo": "bar" }),
                { "code": 200, "method": "post", "data": { "foo":"bar" } })
        self.assertEqual(self.maxcdn.post("/post.json", params={ "foo": "bar" }),
                { "code": 200, "method": "post", "data": { "foo":"bar" } })
        self.assertEqual(self.maxcdn.post("/post.json", params="foo=bar"),
                { "code": 200, "method": "post", "data": { "foo":"bar" } })

    def test_put(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("put"))
        self.assertEqual(self.maxcdn.put("/put.json"),
                { "code": 200, "method": "put", "data": { "foo":"bar" } })

    def test_purge(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("purge"))
        self.assertEqual(self.maxcdn.purge("/purge.json"),
                { "code": 200, "method": "purge", "data": { "foo":"bar" } })

    def test_delete(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("delete"))
        self.assertEqual(self.maxcdn.delete("/delete.json"),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })

        self.assertEqual(self.maxcdn.patch("/delete.json",
                file_or_files="/foo.css"),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })

        self.assertEqual(self.maxcdn.patch("/delete.json",
                file_or_files=["/foo.css", "/bar.css"]),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })

    def test_purge(self):
        requests.Session.request = mock.create_autospec(mock_request,
                return_value=response("delete"))
        self.assertEqual(self.maxcdn.purge(12345),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })
        self.assertEqual(self.maxcdn.purge(12345, "/master.css"),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })
        self.assertEqual(self.maxcdn.purge(12345, ["/master.css", "/other.css"]),
                { "code": 200, "method": "delete", "data": { "foo":"bar" } })

if __name__ == '__main__':
        unittest.main()
