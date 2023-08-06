"""Module Client pour ZentuxLog"""

from zentuxlog_client.errors import AuthMissing


class Settings:
    """
    Définit la configuration que doit appliquer le client.
    """

    def __init__(self,
                 sensor_name,
                 headers=None,
                 timeout=3000,
                 proto='https',
                 version='v1',
                 base_url='api.zentuxlog.net',
                 client_id=None,
                 client_secret=None,
                 username=None,
                 password=None,
                 filePath=None,
                 full=False
                ): # NOQA
        if not headers:
            headers = {
                'Content-Type': "application/json",
                # 'User-Agent': "zentuxlog-client/1.0"
                }
        self.sensor_name = sensor_name
        self.headers = headers
        self.timeout = timeout
        self.proto = proto
        self.version = version
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.filePath = filePath
        self.full = full

    def verify_auth(self):
        if (
            not self.client_id or
            not self.client_secret or
            not self.password or
            not self.username
           ):
            raise AuthMissing("Vérifier vos clés d'authentification")
