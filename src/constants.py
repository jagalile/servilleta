import os


class Configuration():
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__).replace('src', 'configuration'), 'config.ini')
    

class Umbria():
    YOGUR_BASE_URL = 'https://www.comunidadumbria.com/'
    NATILLA_BASE_URL = 'https://natilla.comunidadumbria.com/'