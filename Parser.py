from Company import Company
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logging.basicConfig(level=logging.DEBUG, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")
DOMAIN = "https://www.rusprofile.ru/"


def get_main_requsites(query):
    search_request = "search?query=%s&type=ul&search_inactive=2" % query
    url = DOMAIN + search_request
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    limit = 10

    result = []

    if soup.find("div", class_="main-content search-result emptyresult"):
        return -1
    all_company = soup.findAll('div', class_="company-item", limit=limit)  # <div class="company-item"> 208 строка
    for company in all_company:

        c_text = company.find_next("div", class_="company-item__title").text  # NAME
        u = company.find_next("a", href=True).get("href")  # URL
        a = company.find_next("address", class_="company-item__text").text  # ADDRESS

        inn = company.find_all_next("div", class_="company-item-info", limit=2)  # INN
        for element in inn[1].text.split(
                "\n"):  # Ищем тег класса "company-item-info" во втором элементе массива, так как первый - учредитель либо гендир
            if len(element) == 10:
                try:
                    el = int(element)
                    break
                except ValueError:
                    continue

        result.append(Company([u, c_text.strip(), a.strip(), el]))

    return result


def get_full_requsites(company):
    url = DOMAIN + company.url
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    html = page.content
    soup = BeautifulSoup(html, 'lxml')

    company_info = soup.find('div', class_="tiles")

    full_name = company_info.find_next("div", class_="company-name").text  # FULL NAME
    ogrn = company_info.find_next("span", {"id": "clip_ogrn"}).text  # OGRN
    kpp = company_info.find_next("span", {"id": "clip_kpp"}).text  # KPP
    okved = company_info.find_next("span", class_="bolder").text[1:-1]  # OKVED

    company.full_name = full_name
    company.ogrn = ogrn
    company.kpp = kpp
    company.okved = okved

    return company
