import requests

r = requests.get('https://api.palvelutietovaranto.suomi.fi/api/v11/Service/serviceClass?uri=http%3A%2F%2Furi.suomi.fi%2Fcodelist%2Fptv%2Fptvserclass2%2Fcode%2FP27.1&page=2')
r_dict = r.json()
print(r_dict)

def get_write():
    code =  "P27"
    page = 1
    r = requests.get('https://api.palvelutietovaranto.suomi.fi/api/v11/Service/serviceClass?uri=http%3A%2F%2Furi.suomi.fi%2Fcodelist%2Fptv%2Fptvserclass2%2Fcode%2FP27&page=1')
    r_dict = r.json()
    if r_dict['pageCount'] > 1:
        while page <= r_dict['pageCount']:
            page += 1
            r = requests.get('https://api.palvelutietovaranto.suomi.fi/api/v11/Service/serviceClass?uri=http%3A%2F%2Furi.suomi.fi%2Fcodelist%2Fptv%2Fptvserclass2%2Fcode%2FP27&page={}'.format(page))
            

def clearFile():
    with open("data.txt", "w") as file:
        file.write("")
def writeFile():
    with open("data.txt", "a") as file:
        for l in enumerate(r_dict['itemList']):
            file.write(l.__str__()[l.__str__().find("{"):-1]+"\n")         
def counts():
    with open("data.txt","r") as neat_file:
            for count, line in enumerate(neat_file):
                pass
            print("Amount of results: ", count + 1)
def uniq():
    test_set = set()
    with open("data.txt","r") as file:
        for count, line in enumerate(file):
            test_set.add(line)
    with open("data_final.txt","w") as final_file:
        for count, line in enumerate(test_set):
                final_file.write(line)
    print("Amount of unique results: "+str(test_set.__len__()))

# test()
# clearFile()
# writeFile()
uniq()
# formatFile()
counts()
