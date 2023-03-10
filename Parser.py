from Exceptions.CompanyNotFoundException import CompanyNotFoundException
from Company import Company
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


logging.basicConfig(level=logging.DEBUG, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")


def get_main_requsites(url):
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    limit = 3

    result = []

    if soup.find("div", class_="main-content search-result emptyresult"):
        raise CompanyNotFoundException("Компании с таким названием не найдены")
    all_company = soup.findAll('div', class_="company-item", limit=limit)  # <div class="company-item"> 208 строка
    for company in all_company:

        c_text = company.find_next("div", class_="company-item__title").text  # NAME
        logging.warning("NAME not found") if c_text.strip() is None else logging.info("We've got NAME")

        u = company.find_next("a", href=True).get("href")  # URL
        logging.warning("URL not found") if u is None else logging.info("We've got URL")

        a = company.find_next("address", class_="company-item__text").text  # ADDRESS
        logging.warning("ADR not found") if a.strip() is None else logging.info("We've got ADR")

        inn = company.find_all_next("div", class_="company-item-info", limit=2)  # INN
        for element in inn[1].text.split("\n"):  # Ищем тег класса "company-item-info" во втором элементе массива, так как первый - учредитель либо гендир
            if len(element) == 10:
                try:
                    el = int(element)
                    break
                except ValueError:
                    continue
        if el is None:
            logging.info("INN not found")
        else:
            logging.info("We've got INN")

        result.append(Company([u, c_text.strip(), a.strip(), el]))

    return result
