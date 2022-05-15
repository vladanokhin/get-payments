import re
from typing import Optional
from selenium.webdriver import Firefox
from selenium.common.exceptions import WebDriverException

from _site_exceptions import WrongInstanceBrowser
from configs import SiteConfig


class Site:

    def __init__(self, browser: Firefox):
        self.cfg = SiteConfig()
        self.browser = self.__check_instance(browser)
        self.__check_connection_to_site(self.cfg.SITE_URL)

    @classmethod
    def __check_instance(cls, browser: Firefox) -> Optional[Firefox]:
        if isinstance(browser, Firefox):
            return browser
        else:
            raise WrongInstanceBrowser('Wrong browser instance. Try again.')

    def __check_connection_to_site(self, url: str) -> bool:
        try:
            self.browser.get(url)
            html = self.browser.page_source
            words_list = re.findall(self.cfg.CHECK_SEARCH_WORD, html, re.IGNORECASE)

            if len(words_list) < self.cfg.NUMBER_SEARCHED_WORD:
                raise WebDriverException()

        except WebDriverException:
            print(f'WARNING! Cannot connect to {url}')
            self.browser.close()
            return False

        return True

    def open(self, url: str):
        self.browser.get(url)
