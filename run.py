from sites import SitePaidLikes


if __name__ == '__main__':
    site = SitePaidLikes(check_connection_to_site=True)
    site.auth()
    site.get_payments()

    input('Close browser and exit[enter] > ')
    site.browser_controller.close()
