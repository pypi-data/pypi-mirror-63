"""Module Client pour ZentuxLog"""
import requests
import urllib.parse

from zentuxlog_client.errors import (
    GenericError,
    TimeoutCustomError
)


class EndPoint:
    """Class EndPoint"""

    def __init__(self, settings):
        self.settings = settings

    def get_base_url(self):
        """Méthode qui contruit l'url du EndPoint"""
        return "{proto}://{base_url}".format(
            proto=self.settings.proto,
            base_url=self.settings.base_url,
        )

    def get_uri(self):
        """Méthode qui contruit l'url du EndPoint"""
        return "{base_url}/{version}/".format(
            base_url=self.get_base_url(),
            version=self.settings.version
        )

    def get_url_token(self):
        return urllib.parse.urljoin(self.get_base_url(), '/o/token/')

    def verify_online(self):
        """Vérification de la connexion à l'api."""
        try:
            requests.get(self.get_uri(), timeout=self.settings.timeout)
        except requests.exceptions.Timeout:
            raise TimeoutCustomError("Timeout atteint: {} ms".format(self.settings.timeout))
        except requests.exceptions.RequestException as e:
            raise GenericError("L'api {} n'est pas joignable : {}".format(self.get_uri(), e))
        except Exception as e:
            raise GenericError("Une erreur s'est produite".format(e))
        return True
