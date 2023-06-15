import Exceptions.SearchExceptions
from Company import Company
import logging
import requests
from bs4 import BeautifulSoup
#  import webbrowser
from fake_useragent import UserAgent
from tkinter import messagebox

logging.basicConfig(level=logging.DEBUG, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")
DOMAIN = "https://www.rusprofile.ru/"
UA = UserAgent(use_external_data=True).chrome


def check_connection():
    try:
        requests.head(DOMAIN, timeout=2)
    except requests.ConnectionError as e:
        logging.error(e)
        raise ConnectionError


def get_main_requsites(query):
    check_connection()
    search_request = "search?query=%s&type=ul&search_inactive=2" % query
    url = DOMAIN + search_request
    page = requests.get(url, headers={'User-Agent': UA})
    if page.status_code == 403:
        messagebox.showerror("Ошибка!", "403 ответ от сайта.\n\nОбратитесь к Марселю.")
        exit()
    try:
        if page.history[0].status_code == 302:  # 302 means redirecting to organisation's page if search result is one
            # item. So we call method which returning Company class with full requisites
            return [get_full_requsites(Company([page.url, None, None, None]))]
    except IndexError:
        pass
    except AttributeError as e:
        messagebox.showerror(f"Ошибка!", f"Произошло изменение на rusprofile.ru\n\nОбратитесь к Марселю.\n\n{e}")
        exit()
    html = page.content
    soup = BeautifulSoup(html, 'lxml')
    limit = 10

    result = []

    if soup.find("div", class_="main-content search-result emptyresult"):
        raise Exceptions.SearchExceptions.CompanyNotFoundException
    if soup.find("div", class_="captcha-section"):
        logging.warning("Got captcha")
        raise Exceptions.SearchExceptions.CaptchaEcxcepion
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
    check_connection()
    url = company.url if str(company.url).startswith(DOMAIN) else DOMAIN + company.url
    page = requests.get(url, headers={'User-Agent': UA})
    html = page.content
    soup = BeautifulSoup(html, 'lxml')

    if soup.find("div", class_="captcha-section"):
        logging.warning("Got captcha")
        #  webbrowser.open('https://vk.com', new=2)
        raise Exceptions.SearchExceptions.CaptchaEcxcepion

    company_info = soup.find('div', class_="container")

    name = company_info.find_next("div", class_="company-header__row").get_text()  # NAME
    address = company_info.find_next("span", {"id": "clip_address"}).text  # ADDRESS
    inn = company_info.find_next("span", {"id": "clip_inn"}).text  # INN
    full_name = company_info.find_next("h2", class_="company-name").text  # FULL NAME
    ogrn = company_info.find_next("span", {"id": "clip_ogrn"}).text  # OGRN
    kpp = company_info.find_next("span", {"id": "clip_kpp"}).text  # KPP
    try:
        okved = company_info.find_next("span", class_="bolder").text[1:-1]  # OKVED
    except (TypeError, AttributeError):
        logging.warning("Failed to parse OKVED. What f org is it?")
        raise TypeError("Failed to parse OKVED. What f org is it?")

    company.name = name.strip()
    company.adress = " ".join(address.split())
    company.inn = inn
    company.full_name = full_name
    company.ogrn = str(ogrn)
    company.kpp = str(kpp)
    company.okved = str(okved)

    return company
