import os
from pathlib import Path
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver import Firefox
from typing import Optional

from _browser_exceptions import DriverExistingExcept, BrowserLaunchException
from _site import Site
from configs import BrowserConfig


class BrowserController:

    def __init__(self):
        """
        Class for action with browser
        """
        self.cfg = BrowserConfig
        self.started_browser = False
        self.browser = self.start_up()
        self.site = Site(self.browser)

    def start_up(self) -> Firefox:
        """
        Configure and start up browser Firefox
        :return: Firefox
        """
        if not self.__check_path_to_driver():
            raise DriverExistingExcept(f'Wrong path: {self.cfg.PATH_TO_WEB_DRIVER}. Not found driver!')

        if self.started_browser:
            raise BrowserLaunchException('Error: browser already started. Close browser and try again!')

        browser = Firefox(executable_path=self.cfg.PATH_TO_WEB_DRIVER,
                          service_log_path=self.cfg.LOG_SELENIUM)

        self.started_browser = True
        return browser

    def __check_path_to_driver(self) -> bool:
        """
        Check path to driver
        :return: bool
        """
        path_to_driver = self.cfg.PATH_TO_WEB_DRIVER

        if isinstance(path_to_driver, Path):
            return path_to_driver.is_file() and \
                   path_to_driver.exists()
        else:
            return os.path.isfile(path_to_driver) and \
                   os.path.exists(path_to_driver)

    def close(self) -> bool:
        """
        Closing the browser if it is already running
        :return: bool
        """
        if self.started_browser:
            try:
                self.browser.close()
                self.started_browser = False
            except NoSuchWindowException:
                print('Browsing context has been discarded. Browser may already be closed!')
            return True
        else:
            return False

    def get_browser(self) -> Optional[Firefox]:
        return self.browser
