import json
import requests

class GetZesitmate:
    def __init__(self):
        self.__token_file = './config/token.txt'
        self.__address_file = './data/item.json'
        self.__zestimate_file = './data/zestimate.json'
        with open(self.__token_file, 'r') as f:
            self.__token = f.readline().replace('\n','')

    def get_token(self):
        return self.__token

    def dump_to_file(self, data):
        with open(self.__zestimate_file, 'w') as f:
            json.dump(data, f)

    def request_and_dump_data(self):
        data = list()
        base_url = 'https://api.bridgedataoutput.com/api/v2/zestimates?access_token={}&address={}'
        for line in open(self.__address_file, 'r').readlines():
            address_json = json.loads(line);
            address = address_json['addr']
            url = base_url.format(self.get_token(), address)
            res = requests.get(url)
            res_list = res.json()['bundle']
            if res_list:
                res_dict = res_list[0]
                data.append({'zpid': res_dict['zpid'], 'address': address, 'zestimate': res_dict['zestimate']}) 
        self.dump_to_file(data)            

