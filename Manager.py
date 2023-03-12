import WriterToFile
from Parser import get_main_requsites
from Parser import get_full_requsites
from GUI.MainWindow import MainWindow


def preparse(search_query):
    company_list = get_main_requsites(search_query)
    return company_list


def parse(company):
    try:
        company = get_full_requsites(company)
    except Exception("Error during get full list of requisite") as e:
        raise e
    WriterToFile.make_csv(company)



def get_window():
    mw = MainWindow(preparse, parse)
