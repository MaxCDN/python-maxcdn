#!/usr/bin/env python
import unittest
import time
import os

from maxcdn import MaxCDN


class MaxCDNIntegration(unittest.TestCase):
    def setUp(self):
        self.alias = os.environ["ALIAS"]
        self.key = os.environ["KEY"]
        self.secret = os.environ["SECRET"]
        self.time = str(int(time.mktime(time.gmtime())))

        self.max = MaxCDN(self.alias, self.key, self.secret)

    def test_get(self):
        for end_point in ["account.json",
                          "account.json/address",
                          "users.json",
                          "zones.json"]:
            if "/" in end_point:
                key = end_point.split("/")[1]
            else:
                key = end_point.replace(".json", "")

            rsp = self.max.get(end_point)
            self.assertTrue(rsp["data"][key], "get " + key + " with data")

    def test_get_logs(self):
        rsp = self.max.get("v3/reporting/logs.json")
        self.assertTrue(rsp["next_page_key"],
                        "get v3/reporting/logs.json with data")

    def test_post_and_delete(self):
        data = {"name": self.time, "url": "http://www.example.com/"}
        res = self.max.post("/zones/pull.json", data=data)
        zid = str(res["data"]["pullzone"]["id"])

        rsp = self.max.delete("/zones/pull.json/" + zid)
        self.assertTrue(zid, "post")
        self.assertEqual(200, rsp["code"], "delete")

    def test_put(self):
        street = self.time + "_put"
        rsp = self.max.put("/account.json/address", {"street1": street})
        self.assertEqual(street, str(rsp["data"]["address"]["street1"]))

    def test_purge(self):
        rsp = self.max.get("zones/pull.json")
        zones = rsp["data"]["pullzones"]
        zone = zones[len(zones) - 1]["id"]

        rsp = self.max.purge(zone)
        self.assertEqual(200, rsp["code"])

        rsp = self.max.get("reports/popularfiles.json")
        popularfiles = rsp["data"]["popularfiles"]

        rsp = self.max.purge(zone, popularfiles[0]["uri"])
        self.assertEqual(200, rsp["code"])

        files = [popularfiles[0]["uri"], popularfiles[1]["uri"]]
        rsp = self.max.purge(zone, files)
        self.assertEqual(200, rsp["code"])

if __name__ == '__main__':
        unittest.main()
