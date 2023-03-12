import os

def make_csv(company):
    path = os.getcwd() + "\\Results\\"
    if not os.path.isdir(path):
        os.mkdir(path)
    file = company.name.replace('"', "'") + ".csv"
    name = path + file

    with open(name, 'w') as f:
        f.write("Название;Полное название;Адрес;ИНН;ОГРН;КПП;ОКВЭД\n%s;%s;%s;%s;%s;%s;%s" % (
            company.name,
            company.full_name,
            company.adress,
            company.inn,
            company.ogrn,
            company.kpp,
            company.okved
        ))
        f.close()
