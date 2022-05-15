from time import sleep

from ._site import Site
from configs import SiteConfig


class SitePaidLikes(Site):
    cfg = SiteConfig()

    selectors = {
        'login_button': '.container .top_header .login > a:last-child',
        'user_email': 'form label > input[name="email"]',
        'user_password': 'form label > input[name="password"]',
        'signin_button': 'form > button.button',
        'max_points': '.container .user-control > a > span',
        'points_input': 'div.four > form input[name="payout_int"]',
        'method_payment_out_paypal': 'div.four > form > label[for="radio1"] > input[name="payout_method"]',
        'method_payment_out_bank': 'div.four > form > label[for="radio3"] > input[name="payout_method"]',
        'submit_payment_out_button': 'div.four > form > input[name="submit"]'
    }

    def __init__(self, **kwargs):
        super().__init__(self.cfg.SITE_URL, **kwargs)

        self.authenticated_url = '/memberarea'
        self.is_authorized = self._is_authorized()

    def _is_authorized(self) -> bool:
        return self.check_attribute_value(self.selectors['login_button'],
                                          'href',
                                          self.authenticated_url)

    def auth(self) -> bool:
        if not self.is_authorized:
            self.click_element_by_selector(self.selectors['login_button'])
            self.input_text_by_selector(self.selectors['user_email'], self.cfg.USER_EMAIL)
            self.input_text_by_selector(self.selectors['user_password'], self.cfg.USER_PASSWORD)
            self.click_element_by_selector(self.selectors['signin_button'])

            sleep(1.5)
            if self._check_current_url_path(self.authenticated_url):
                self.is_authorized = True
                return True

        return False

    def get_max_points(self) -> str:
        if not self.is_authorized:
            return str(0)
        tag_text = self.get_text_by_selector(self.selectors['max_points'])

        if tag_text:
            return str(tag_text)

    def get_payments(self) -> bool:
        self._open(self.cfg.PAYMENT_URL)
        self.input_text_by_selector(self.selectors['points_input'], self.get_max_points())

        selector_method = self.selectors['method_payment_out_bank']

        if self.cfg.PAYMENT_OUT_METHOD == 'paypal':
            selector_method = self.selectors['method_payment_out_paypal']

        self.click_element_by_selector(selector_method)
        self.click_element_by_selector(self.selectors['submit_payment_out_button'])

        return True
