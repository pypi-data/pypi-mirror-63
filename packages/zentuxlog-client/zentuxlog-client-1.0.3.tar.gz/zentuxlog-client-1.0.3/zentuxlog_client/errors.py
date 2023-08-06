"""Module d'erreurs."""


class GenericError(Exception):
    """Erreur générique."""
    pass


class AuthMissing(Exception):
    """Manque de clés d'authentification."""
    pass


class ResponseCodeError(GenericError):
    """Erreur liée à l'analyse de réponse."""
    def __init__(self, code, msg=''):
        self.msg = "Réponse incorrecte. Status {st}. Description : {desc}".format(
            st=code,
            desc=msg
            )

    def __str__(self):
        return self.msg


class TimeoutCustomError(GenericError):
    """Erreur customisée pour la gestion du timeout."""
    pass


class RequestError(GenericError):
    """Erreur de communication avec l'API."""
    def __init__(self, msg=''):
        self.msg = "Erreur de communication avec l'API : {msg}".format(msg=msg)

    def __str__(self):
        return self.msg
