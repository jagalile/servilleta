import configparser

from src.constants import Configuration, Umbria
from src.web_scraper import WebScraper


class Servilleta():

    def __init__(self, yogur=False):
        self.username = None
        self.password = None
        self.scraper = WebScraper(headless=False)
        self.yogur = yogur
        self.base_url = None
        
    def get_credentials(self):
        config = configparser.ConfigParser()
        config.read(Configuration.CONFIG_FILE_PATH)
        config.sections()
        
        self.username = config['CREDENTIALS']['user']
        self.password = config['CREDENTIALS']['pass']
        
    def get_umbria_base_url(self):
        self.base_url = Umbria.YOGUR_BASE_URL if self.yogur else Umbria.NATILLA_BASE_URL

    def login_umbria(self):
        self.get_credentials()
        self.get_umbria_base_url()
        self.scraper.start_connection(self.base_url)
        self.scraper.fill_login_form(self.username, self.password)
        
if __name__ == "__main__":
    servilleta = Servilleta(yogur=True)
    servilleta.login_umbria()