[![pipeline status](https://gitlab.django-creation.net/zentux/zentuxlog-client/badges/master/pipeline.svg)](https://gitlab.django-creation.net/zentux/zentuxlog-client/commits/master)
[![coverage report](https://gitlab.django-creation.net/zentux/zentuxlog-client/badges/master/coverage.svg)](https://gitlab.django-creation.net/zentux/zentuxlog-client/commits/master)


# Utilisation
## Dans un script, une classe, un module, ...

```python
from zentuxlog_client.client import Client

APIKEY = "hkhfds56dfsdfjhdjk"
APISECRET = "KAP0dika43iH7"
USERNAME = "John"
PASSWORD = "Mypass

auth = {
            'client_id': APIKEY,
            'client_secret': APISECRET,
            'username': USERNAME,
            'password': PASSWORD
        }
c = Client(auth=auth)
c.send(data="information à logguer", method="POST", path="logs/")
```

## Dans une exception personnalisée
```python
from zentuxlog_client.client import Client

APIKEY = "hkhfds56dfsdfjhdjk"
APISECRET = "KAP0dika43iH7"
USERNAME = "John"
PASSWORD = "Mypass"
auth = {
            'client_id': APIKEY,
            'client_secret': APISECRET,
            'username': USERNAME,
            'password': PASSWORD
        }
c = Client(auth=auth)

class MyCustomError(Exception):
    """Erreur générique."""
    def __init__(self, msg=''):
        self.msg = msg
        if msg:
            c.send(msg, method="POST", path="logs/")

    def __str__(self):
        return self.msg

```
