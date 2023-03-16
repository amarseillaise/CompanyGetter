import os
import xml.etree.ElementTree as xml


def make_xml(company):
    # path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "\\Results\\"
    path = os.getcwd() + "\\Results\\"

    if not os.path.isdir(path):
        os.mkdir(path)
    file = company.name.replace('"', "'") + ".xml"
    name = path + file

    org = xml.Element("organisation")

    n = xml.SubElement(org, "name")
    n.text = company.name

    fn = xml.SubElement(org, "full_name")
    fn.text = company.full_name

    a = xml.SubElement(org, "address")
    a.text = company.adress

    i = xml.SubElement(org, "inn")
    i.text = str(company.inn)

    og = xml.SubElement(org, "ogrn")
    og.text = company.ogrn

    k = xml.SubElement(org, "kpp")
    k.text = company.kpp

    ok = xml.SubElement(org, "okved")
    ok.text = company.okved

    tree = xml.ElementTree(org)
    tree.write(name)
