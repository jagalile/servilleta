import os
from sys import platform
import requests
import zipfile
import configparser
import logging
import urllib.request
from urllib.error import HTTPError
from requests.exceptions import InvalidURL

from src.constants import Configuration


class Driver():
    
    _LINUX = 'chromedriver_linux64.zip'
    _DARWIN = 'chromedriver_mac64.zip'
    _WIN32 = 'chromedriver_win32.zip'
    _CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__).replace('src', 'chromedriver'))
    
    def __init__(self):
        self.driver_url = self._get_driver_url()
        self.browser_version = self._get_chrome_version()
        self.driver_file = None
        
    def _get_driver_url(self):
        config = configparser.ConfigParser()
        config.read(Configuration.CONFIG_FILE_PATH)
        config.sections()
        
        return config['CHROMEDRIVER']['url']
        
    
    def _extract_version(self, output):
        try:
            google_version = ''
            for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
                if letter != '\n':
                    google_version += letter
                else:
                    break
            return(google_version.strip())
        except TypeError:
            return

    def _get_chrome_version(self):
        version = None
        install_path = None

        try:
            if platform == "linux" or platform == "linux2":
                # linux
                install_path = "/usr/bin/google-chrome"
            elif platform == "darwin":
                # OS X
                install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
            elif platform == "win32":
                # Windows
                stream = os.popen(
                        'reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows'
                        '\\CurrentVersion\\Uninstall\\Google Chrome"'
                    )
                output = stream.read()
                version = self._extract_version(output)
        except Exception as ex:
            print(ex)

        version = os.popen(f"{install_path} --version").read().strip('Google Chrome ').strip() if install_path else version

        return version
    
    def _download_driver(self):
        if platform == "linux" or platform == "linux2":
            so = self._LINUX
        elif platform == "darwin":
            so = self._DARWIN
        elif platform == "win32":
            so = self._WIN32
        else: raise
        
        try:
            download_url = self.driver_url.format(self.browser_version, so)
            self._check_url(download_url)
            self._create_driver_folder()
            self.driver_file = os.path.join(self._CHROMEDRIVER_PATH, 'chromedriver.zip')
            
            response = requests.get(download_url)
            open(self.driver_file, 'wb').write(response.content)
        except InvalidURL:
            print('Invalid chromedriver url {}'.format(self.driver_url.format(self.browser_version, so)))
        
    def _create_driver_folder(self):
        if not os.path.exists(self._CHROMEDRIVER_PATH):
            os.mkdir(self._CHROMEDRIVER_PATH)
        
    def _extract_file(self):
        if self.driver_file is None:
            logging.error('Driver file not found')
            raise
        with zipfile.ZipFile(self.driver_file, 'r') as zip_ref:
            zip_ref.extractall(self._CHROMEDRIVER_PATH)
        os.remove(self.driver_file)
    
    def _check_url(self, url):
        try:
            urllib.request.urlopen(url).getcode()
        except HTTPError as e:
            logging.exception('Chromedriver url: {} with code: {}'.format(url, e))

    def get_driver(self):
        self._download_driver()
        self._extract_file()