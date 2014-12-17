import os
from maxcdn import MaxCDN

alias = os.environ["ALIAS"]
key = os.environ["KEY"]
secret = os.environ["SECRET"]
maxcdn = MaxCDN(alias, key, secret)

def get_logs():
    maxcdn.get("v3/reporing/logs.json")

def get_users():
    maxcdn.get("users.json")

def get_account():
    maxcdn.get("account.json")

def get_pullzones():
    maxcdn.get("zones/pull.json")


if __name__ == '__main__':
    import timeit

    for f in [ 'get_logs',
            'get_users',
            'get_account',
            'get_pullzones' ]:
        t = timeit.Timer(f + "()", setup = "from __main__ import " + f)
        print("%-20s %5.0fms" % (f + ":", (t.timeit(number=1) * 1000)))

