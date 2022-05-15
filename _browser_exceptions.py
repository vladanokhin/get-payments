from selenium.common.exceptions import WebDriverException


class BrowserLaunchException(WebDriverException):
    """
    Browser launch exception
    """


class DriverExistingExcept(WebDriverException):
    """
    Browser driver not found
    """