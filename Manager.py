from Exceptions import SearchExceptions

import Exceptions.SearchExceptions
import WriterToFile
from Parser import get_main_requsites
from Parser import get_full_requsites
from GUI.MainWindow import MainWindow


def preparse(search_query):
    try:
        company_list = get_main_requsites(search_query)
    except (ConnectionError, SearchExceptions.CompanyNotFoundException, SearchExceptions.CaptchaEcxcepion) as e:
        raise e
    return company_list


def parse(company):
    try:
        company = get_full_requsites(company)
    except (ConnectionError, SearchExceptions.CompanyNotFoundException, SearchExceptions.CaptchaEcxcepion) as e:
        raise e
    except TypeError:
        raise TypeError
    WriterToFile.make_xml(company)



def get_window():
    mw = MainWindow(preparse, parse)
