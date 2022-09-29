from genericpath import isfile
import os

from click import option
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from src.driver import Driver


class WebScraper():
    
    def __init__(self, headless=True, muted=True):
        self.headless = headless
        self.muted = muted
        self.options = self._set_webdriver_options
        self.driver = self._chromedriver_driver

    @property
    def _set_webdriver_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        if self.headless:
            options.add_argument("--headless")
        if self.muted:
            options.add_argument("--mute-audio")
        
        return options

    @property
    def _chromedriver_driver(self):
        try:
            return webdriver.Chrome(self._driver_path(), chrome_options=self.options)
        except:
            Driver().get_driver()
            return webdriver.Chrome(self._driver_path(), chrome_options=self.options)

    def _driver_path(self):
        driver_path = os.path.join(os.path.dirname(__file__).replace('src', 'chromedriver'), 'chromedriver')
        
        if os.path.isfile(driver_path):
            return driver_path
        else:
            raise Exception('Chromedriver missing!')
 
    def start_connection(self, url):
        self.driver.get(url)

    def click_element(self, element):
        try:
            element = self.driver.execute_script("arguments[0].click();", element)
        except WebDriverException:
            print('Element is not clickable')
    
    def fill_login_form(self, username, password):
        login_username = self.driver.find_element(By.NAME, 'ACCESO').send_keys(username)
        login_password = self.driver.find_element(By.NAME, 'CLAVE').send_keys(password)
        submit = self.driver.find_element(By.XPATH, '//*[@id="login"]/form/p[3]/input')
        self.click_element(submit)
    
    def close_connection(self):
        self.driver.quit()