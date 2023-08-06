import time
import logging


class Data:
    """
    Classe qui permet de récupérer les logs d'un fichier log spécifié.
    Elle retourne la dernière ligne ou la totalité du fichier log sous la forme d'une chaine de caractères.
    """

    def __init__(self, path, delay=5, full=False):
        self.delay = delay
        self.full = full
        self.path = path

        logging.basicConfig(
            filename="zentuxlog_client/data.log",
            level=logging.WARNING,
            format='%(asctime)s : %(levelname)s : %(message)s'
        )

    def generate(self, daemon=True):
        """
        Générateur qui retourne les lignes d'un fichier log entièrement ou non, en fonction de self.full,
        puis retourne les nouvelles lignes.
        """
        try:
            with open(self.path, 'r') as file:
                if not self.full:
                    file.seek(0, 2)
                while 1:
                    line = file.readline()
                    if not line:
                        if not daemon:
                            break
                        time.sleep(self.delay)
                    else:
                        yield line
        except IOError as e:
            logging.error("Problem with file. {exception}".format(
                exception=e
            ))
