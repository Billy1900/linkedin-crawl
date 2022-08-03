from linkedinCrawler import Crawler


def driver_main():
    linkedin = Crawler()
    linkedin.profile_info("https://www.linkedin.com/in/zhilong-wang-996498162/")


if __name__ == '__main__':
    driver_main()

