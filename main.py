from linkedinCrawler import Crawler


def driver_main():
    linkedin = Crawler()
    linkedin.profile_info("the profile url you want to crawl")


if __name__ == '__main__':
    driver_main()

