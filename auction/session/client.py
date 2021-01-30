import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver


class Client:
    SCROLL_PAUSE_TIME = 1
    CHROME_PATH = os.path.dirname(__file__) + '\chromedriver.exe'

    def __init__(self):
        """A selenium client
        """
        self.driver = self.create_driver()

    def run(self, url: str, scroll: bool, quit: bool) -> BeautifulSoup:
        """Get html of a page using selenium

        Args:
            url (str): Url to scrap
            scroll (bool): If true, scroll down the page to get more data
            quit (bool): If true, quit the driver

        Returns:
            BeautifulSoup: Pretty html response
        """
        self.driver.get(url)
        time.sleep(1)
        if scroll:
            self.scroll_down()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        if quit:
            self.driver.quit()
        return soup

    def create_driver(self):
        """Create driver with options

        """
        self.profile = webdriver.ChromeOptions()
        self.profile.add_argument('headless')
        driver = webdriver.Chrome(
            options=self.profile,
            executable_path=self.CHROME_PATH)
        return driver

    def scroll_down(self):
        """Scroll down the page to get more data

        """
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight"
        )

        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                break
            last_height = new_height
