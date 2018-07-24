import urllib.parse
import logging
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-setuid-sandbox')

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
log = logging.getLogger(__name__)


class Spooky(object):
    driver = None

    def __init__(self, cookie=None):
        if self.driver is None:
            # TODO: fix the phantomJS page rendering
            self.driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=d)
            self.driver.set_page_load_timeout(10)
            self.driver.set_window_size(1024, 768)

        if cookie:
            self.driver.get(cookie.get("domain"))
            cookie['domain'] = None  # Clear the domain and use the current page
            self.driver.add_cookie(cookie)

    def __enter__(self):
        return self.driver

    def __exit__(self, type, value, traceback):
        self.driver.close()
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)

    @staticmethod
    def make_cookie(domain, name, value, secure=False):
        ret = {
            'domain': domain,
            'name': name,
            'value': value,
            'secure': secure
        }
        return ret


def get(url):
    with Spooky() as s:
        s.get(url)


def xss_get(url,
            cookie_domain=None,
            cookie_name=None,
            cookie_value=None,
            user_agent=None):
    cookie = None
    if cookie_domain:
        base_url = urllib.parse.urlparse(cookie_domain)
        domain = "{}://{}".format(base_url.scheme, base_url.netloc)
        cookie = Spooky.make_cookie(domain, cookie_name, cookie_value)

    with Spooky(cookie) as s:
        log.critical("Fetching: {}".format(url))
        try:
            s.get(url)
        except Exception as e:
            log.exception("Some exception occured. we're ignoring")

        log.critical(s.page_source)
        for entry in s.get_log("browser"):
            log.critical(entry)
        time.sleep(5)
        log.critical("Done")
