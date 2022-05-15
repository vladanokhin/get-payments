from pathlib import Path


class BrowserConfig:
    PATH_TO_WEB_DRIVER = Path('drivers/geckodriver_mac')

    LOG_SELENIUM = Path('logs/browser.log')


class SiteConfig:
    SITE_URL = 'https://www.paidlikes.de'

    CHECK_SEARCH_WORD = 'paidlikes.de'  # We will search for this word in html to check if the site is working correctly

    NUMBER_SEARCHED_WORD = 3
