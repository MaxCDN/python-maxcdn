#We're Hiring!
Do you like building cool stuff?  Do APIs keep you up at night? We're looking for our next superstar hacker and you could be it. Interested? Check out our job posting on [stackoverflow](http://careers.stackoverflow.com/jobs/37078/senior-web-engineer-for-fun-growing-la-startup-maxcdn&a=JdFbT4OY).

# MaxCDN REST Web Services Python Client

[![Build Status](https://travis-ci.org/jmervine/python-maxcdn.png?branch=master)](https://travis-ci.org/jmervine/python-maxcdn)

> TODO: Support Python 3.x

## Installation

```
sudo pip install maxcdn # coming soon
```

## Usage
```python
from maxcdn import MaxCDN

api = MaxCDN("myalias", "consumer_key", "consumer_secret")

# Get Account Info
api.get("/account.json")

# Create Pull Zone
api.post("/zones/pull.json", {'name': 'mypullzone', 'url': 'http://yourorigin.com', 'compress': '1'})

# Update Pull Zone
api.put("/zones/pull.json/12345", {'url': 'http://neworigin.com'})

# Purge All Cache
api.delete("/zones/pull.json/12345/cache")

# Purge File
api.delete("/zones/pull.json/77573/cache", data={'file': '/my-file.png'})

```

## Methods
It has support for `GET`, `POST`, `PUT` and `DELETE` OAuth signed requests.

### We now have a shortcut for Purge Calls!
```python
zone_id = 12345

# Purge Zone
api.purge(zone_id)

# Purge File
api.purge(zone_id, '/some_file')

# Purge Files
api.purge(zone_id, ['/some_file', '/another_file'])
```

Every request can take an optional debug parameter.
```python
api.get("/account.json", debug=True)
# Will output
# Making GET request to http://rws.netdna.com/myalias/account.json
#{... API Returned Stuff ...}

Every request can also take an optional debug_json parameter if you don't like the exception based errors.
api.get('/account.json', debug_json=True)
```

For more information about what optional parameters this methods accept you
should check out [@kennethreitz](http://github.com/kennethreitz) library
[Requests](https://github.com/kennethreitz/requests).

## Initialization
For applications that don't require user authentication,
you can use the default initialization as the example above.

For applications that require user authentication, you can
initialize the API as follows.

```python
api = MaxCDN("myalias", "consumer_key", "consumer_secret",
             token="user_token", token_secret="user_token_secret")
```

You can also send the optional parameter header_auth, which takes a boolean
to send the OAuth header in the body or URLEncoded.

# Development

```
git clone https://github.com/jmervine/python-maxcdn.git

make          # setup and test
make setup    # installation w/ deps
make test     # test w/ primary python
make int      # integration tests w/ primary python
make test/all # test w/ python2 python3.2 python3.3 python3.4
make int      # integration tests
make int/all  # integration w/ python2 python3.2 python3.3 python3.4
make nose     # verbose test output w/ nosetests
```

