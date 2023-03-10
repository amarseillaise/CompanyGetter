class Company:
    def __init__(self, requsites):
        self.url = requsites[0]
        self.name = requsites[1]
        self.adress = requsites[2]
        self.inn = requsites[3]
        self.full_name = None
        self.kpp = None
        self.ogrn = None
        self.okved = None