from Parser import get_main_requsites
from Exceptions.CompanyNotFoundException import CompanyNotFoundException
def start():
    domain = "https://www.rusprofile.ru"
    search_query = "мишн фудс"
    url = "%s/search?query=%s&type=ul&search_inactive=2" % (domain, search_query)
    company_list = []
    try:
        company_list = get_main_requsites(url)
    except CompanyNotFoundException:
        print("catched")
    for j in company_list:
        print(j.name, j.url, j.adress, j.inn)
