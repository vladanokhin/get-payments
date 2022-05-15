from browser import BrowserController


if __name__ == '__main__':
    browser = BrowserController()
    # print(browser.site.check_connection_to_site(browser.cfg.SITE_URL))

    input('Close browser and exit[enter] > ')
    browser.close()
