import glob
import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from browser import Browser
from UserInfo import secret
from utils import RetryException, retry


class Logging(object):
    PREFIX = "linkedin-crawler"

    def __init__(self):
        try:
            timestamp = int(time.time())
            self.cleanup(timestamp)
            self.logger = open("/tmp/%s-%s.log" % (Logging.PREFIX, timestamp), "w")
            self.log_disable = False
        except Exception:
            self.log_disable = True

    def cleanup(self, timestamp):
        days = 86400 * 7
        days_ago_log = "/tmp/%s-%s.log" % (Logging.PREFIX, timestamp - days)
        for log in glob.glob("/tmp/linkedin-crawler-*.log"):
            if log < days_ago_log:
                os.remove(log)

    def log(self, msg):
        if self.log_disable:
            return

        self.logger.write(msg + "\n")
        self.logger.flush()

    def __del__(self):
        if self.log_disable:
            return
        self.logger.close()


class Crawler(Logging):
    URL = "https://www.linkedin.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=True):
        super(Crawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0
        self.login()

    def login(self):
        browser = self.browser
        url = Crawler.URL + "/uas/login"
        browser.get(url)
        u_input = browser.find_one('input[id="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[id="password"]')
        p_input.send_keys(secret.password)

        login_btn = browser.find_one('button[aria-label="Sign in"]')
        login_btn.click()

        @retry()
        def check_login():
            if browser.find_one('input[id="username"]'):
                raise RetryException()

        check_login()
    
    def profile_list(self, url):
        url_list = []
        self.browser.driver.get(url)
        profile_section = self.browser.driver.find_elements(By.XPATH, '//*[@class="entity-result__title-text t-16"]/a')

        for item in profile_section:
            url_list.append(item.get_attribute("href"))

        return url_list
    
    def get_follower_list(self):
        follower_url_set = set()
        follower_url = "https://www.linkedin.com/feed/followers/"
        self.browser.driver.get(follower_url)

        # Get scroll height
        last_height = self.browser.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.browser.scroll_down()

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
                
            followers_section = self.browser.driver.find_elements(By.XPATH, '//*[@class="follows-recommendation-card__info"]/a')

            for item in followers_section:
                follower_url_set.add(item.get_attribute("href"))
    
        return follower_url_set

    def profile_info(self, url):
        self.browser.driver.get(url)
        # name, //*[@id="ember36"]/div[2]/div[2]/div[1]/div[1]/h1
        name = self.browser.driver.find_element(By.XPATH, '//*[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]')
        if name is None:
            name = 'Name None'
        else:
            name = name.text.strip()
        print(name)
        # overview
        overview = self.browser.driver.find_element(By.XPATH, '//*[@class="text-body-medium break-words"]')
        if overview is None:
            overview = 'Overview None'
        else:
            overview = overview.text.strip()
        print(overview)

        # location
        location = self.browser.driver.find_element(By.XPATH, '//*[@class="text-body-small inline t-black--light break-words"]')
        if location is None:
            location = 'Location None'
        else:
            location = location.text.strip()
        print(location)

        # about
        try:
            about = self.browser.driver.find_element(By.XPATH,
                                                 '//*[@class="artdeco-card ember-view relative break-words pb3 mt2 "]/div[3]/div/div/div/span[1]')
        except NoSuchElementException:
            about = None

        if about is None:
            about = 'About None'
        else:
            about = about.text.strip()
        print(about)

        # experience
        sections = self.browser.driver.find_elements(By.XPATH,
                                                    '//*[@class="artdeco-card ember-view relative break-words pb3 mt2 "]/div[3]/ul/li')
        if sections is None:
            sections = 'Section None'

        edu = []
        experience = []
        for section in sections:
            section = section.text
            # de-duplication
            item_list = section.split("\n")
            single_item_str = ''
            for idx, item in enumerate(item_list):
                if idx % 2 == 0:
                    single_item_str += item
                    single_item_str += ","

            # there are some people do not add the year of entering college, though not convincing, but still crawl
            # MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            # cnt_month = 0
            # for it in MONTH:
            #     if it.lower() not in single_item_str.lower():
            #         cnt_month += 1
            #
            # if cnt_month == 12:
            #     continue  # skip those which do not have date string

            if "university" in single_item_str.lower() or "college" in single_item_str.lower():
                edu.append(single_item_str)
            elif "intern" in single_item_str.lower() or "full-time" in single_item_str.lower() or "Quant" in single_item_str.lower() or "Quantitative" in single_item_str.lower() or "Research" in single_item_str.lower():
                experience.append(single_item_str)

        print(experience)
        print("=================")
        print(edu)
