import re
from typing import Optional
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from browser import BrowserController
from configs import SiteConfig


class Site:

    cfg = SiteConfig()

    def __init__(self, url: str, browser_controller: BrowserController = None, check_connection_to_site=False):
        self.url = url or self.cfg.SITE_URL

        self.browser_controller = self.__check_instance(browser_controller)
        self.browser = self.browser_controller.get_browser()

        if check_connection_to_site:
            self.__check_connection_to_site(self.url)
        else:
            self._open(self.url)

    @classmethod
    def __check_instance(cls, browser: Optional[BrowserController]) -> BrowserController:
        if isinstance(browser, BrowserController):
            return browser
        else:
            return BrowserController()

    def __check_connection_to_site(self, url: str) -> bool:
        try:
            self._open(url)
            if not self.__is_correct_web_page():
                raise WebDriverException()
        except WebDriverException:
            print(f'WARNING! Cannot connect to {url}')
            self.browser_controller.close()
            return False

        return True

    def __is_correct_web_page(self) -> bool:
        """
        Looking for words in html which indicate that the open site is correct
        :return: bool
        """
        html = self.browser.page_source
        words_list = re.findall(self.cfg.CHECK_SEARCH_WORD, html, re.IGNORECASE)
        if len(words_list) < self.cfg.NUMBER_SEARCHED_WORD:
            return False
        else:
            return True

    def _open(self, url: str) -> None:
        """
        Open a web page in a browser
        :param url: site url
        :return: None
        """
        self.browser.get(url)

    def __find_element(self, css_selector: str, timeout: int = 5, ) -> Optional[WebElement]:
        """
        Search element in html by css selector
        :param css_selector: css selector, example: '.container > a'
        :param timeout: time to searching element
        :return: None or WebElement
        """
        try:
            wait = WebDriverWait(self.browser, timeout)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            return element
        except (NoSuchElementException, TimeoutException):
            return None

    def check_attribute_value(self, css_selector: str, attr: str, value: str) -> bool:
        if not self.__is_correct_web_page():
            return False

        element = self.__find_element(css_selector)
        if isinstance(element, WebElement):
            return element.get_dom_attribute(attr) == value
        else:
            return False

    def click_element_by_selector(self, css_selector: str) -> bool:
        element = self.__find_element(css_selector)
        if isinstance(element, WebElement):
            element.click()
            return True

        return False

    def input_text_by_selector(self, css_selector: str, text: str) -> bool:
        element = self.__find_element(css_selector)
        if isinstance(element, WebElement):
            element.send_keys(text)
            return True

        return False

    def get_text_by_selector(self, css_selector: str) -> str:
        element = self.__find_element(css_selector)
        if isinstance(element, WebElement):
            return element.text

        return ''

    def _get_current_url(self) -> str:
        return self.browser.current_url

    def _check_current_url_path(self, path):
        url = urlparse(self.browser.current_url)

        return url.path == path

    def _get_browser_controller(self):
        return self.browser_controller
