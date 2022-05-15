from pathlib import Path


class BrowserConfig:
    PATH_TO_WEB_DRIVER = Path('drivers/geckodriver_mac')

    LOG_SELENIUM = Path('logs/browser.log')


class SiteConfig:
    SITE_URL = 'https://www.paidlikes.de'
    PAYMENT_URL = 'https://paidlikes.de/memberarea/auszahlung'

    CHECK_SEARCH_WORD = 'paidlikes.de'  # We will search for this word in html to check if the site is working correctly

    NUMBER_SEARCHED_WORD = 3

    USER_EMAIL = 'vladanoxun@gmail.com'

    USER_PASSWORD = 'Anikron009'

    PAYMENT_OUT_METHOD = 'paypal'  # payment output method by PayPal

    # PAYMENT_OUT_METHOD = 'bank' # payment output method by bank
