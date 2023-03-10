from Exceptions import CompanyNotFoundException
import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logging.basicConfig(level=logging.ERROR, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")


def get_main_requsites(url):
    page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    result = {"company_url": None,
              "company_name": None,
              "company_adress": None,
              "company_inn": None}

    if soup.find("div", class_="main-content search-result emptyresult"):
        raise CompanyNotFoundException
    all_company = soup.findAll('div', class_="company-item")  # <div class="company-item__title"> 150 строка
    for company in all_company:

        if company.find('div', class_="company-item__title"):
            for company_name in company:  # Try to find the NAME and ID

                if company_name.find('span', class_="finded-text"):  # NAME
                    c_text = company_name.text
                    if r"'\n" in c_text:
                        c_text.replace(r"'\n", "")
                    if r"\n'" in c_text:
                        c_text.replace(r"\n'", "")
                    result["company_name"] = c_text
                    logging.info("We've got the NAME")
                else:
                    logging.warning("The NAME is not found")

                if company_name.find("a", href=True):
                    result["company_url"] = company["href"]
                    logging.info("We've got the URL")
                else:
                    logging.warning("The URL is not found")
    print(result)