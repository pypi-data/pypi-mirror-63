import requests
from json import loads, dumps

class Cloudv:
    def __init__(self, var_name):
        self.variables = "http://106.13.179.116:39999/variables"
        self.var_name = var_name    # instance variable unique to each instance

    def update(self, value):
        url = self.variables+'/'+self.var_name
        requests.put(url,data={'data':dumps(value)})

    def get(self):
        url = self.variables+'/'+self.var_name
        response = requests.get(url)
        return loads(response.json())

    def __repr__(self):
        return str(self.get())
    

test_data = ['hello world', None, 1234.445, [123,'123'], {'va1':123213,'var':'hello weold'}]

if __name__ == "__main__":
    i = Cloudv('test')
    i.update(123456)
    print(i.get())