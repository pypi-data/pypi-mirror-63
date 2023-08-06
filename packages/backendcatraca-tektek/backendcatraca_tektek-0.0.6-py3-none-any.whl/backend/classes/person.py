class Person():
    def __init__(self, person_cod, person_name):
        self.person_cod = person_cod
        self.person_name = person_name
        pass

    def get_person_name(self):
        return self.person_name
        
    def get_person_cod(self):
        return self.person_cod