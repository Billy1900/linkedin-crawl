from linkedinCrawler import Crawler


def get_profile_list(linkedin):
    keywords = "quant"
    profile_list = []

    for num in range(1, 3):
        url = "https://www.linkedin.com/search/results/people/?keywords=" + keywords + "&origin=SWITCH_SEARCH_VERTICAL" + "&page=" + str(
            num)
        url_list = linkedin.profile_list(url)
        for i in url_list:
            profile_list.append(i)

    return profile_list


def driver_main():
    linkedin = Crawler()
    # profile_list = get_profile_list(linkedin)
    # print(profile_list)
    # if len(profile_list) == 0:
    #     print("profile list is 0")
    #     return

    # for url in profile_list:
    #     linkedin.profile_info(str(url))

    follower_list = linkedin.get_follower_list()
    print(len(follower_list))
    for url in follower_list:
        print(url)


if __name__ == '__main__':
    driver_main()
