import time
import threading
import random
import requests
from decouple import config
import json

from classes.person import Person


class PersonManager():

    def __init__(self):       
        self.person = []

    def get_person(self):
        r = requests.get(config("GET_ORDERS")+"orders") 
        data  = r.json()
        order_list = data['items']
        return order_list

    def get_person_name(person_cod):

        headers = {'content-type': 'application/json'}
        data = {
            "CDFUNC": person_cod 
        }        
        r = requests.post(config("API_ADDRESS")+"operador",headers=headers, data=json.dumps(data))
        data  = r.json()
        return data["NMFUNC"]
  