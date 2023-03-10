from Parser import get_main_requsites
def start():
    domain = "https://www.rusprofile.ru"
    search_query = "аэросила"
    url = "%s/search?query=%s&type=ul&search_inactive=2" % (domain, search_query)
    top3_list = get_main_requsites(url)
