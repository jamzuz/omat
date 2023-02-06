import requests
import pandas


def clear_file():
    # Write a line in file overwriting it completely
    with open("data.txt", "w") as file:
        file.write("")


def write_file(data, file_name="data.txt"):
    # open .txt file in append mode
    with open(file_name, "a") as file:
        # write itemlist IDs in the file
        for obj in data['itemList']:
            file.write(obj['id'] + "\n")


def counts():
    # Count lines in file
    with open("data.txt", "r") as neat_file:
        for count in enumerate(neat_file):
            pass
        print("Amount of results: ", count[0] + 1)


def uniq():
    # Check for unique lines in file by inserting every line into a set which only accepts unique values
    id_set = set()
    with open("data.txt", "r") as file:
        for line in file:
            id_set.add(line)
    # write unique IDs in another file
    with open("data_final.txt", "w") as final_file:
        for obj in id_set:
            final_file.write(obj)
    print("Amount of unique results: "+str(id_set.__len__()))

def main():
    clear_file()
    codes = ["P27", "P27.1"]
    for count, code in enumerate(codes):
        url = "https://api.palvelutietovaranto.suomi.fi/api/v11/Service/serviceClass?uri=http%3A%2F%2Furi.suomi.fi%2Fcodelist%2Fptv%2Fptvserclass2%2Fcode%2F{}".format(
            code)
        page = 1
        while True:
            params = {"page": page}
            response = requests.get(url, params=params)
            data = response.json()

            write_file(data, str(codes[count-1])+".txt")
            if len(data['itemList']) < 1000 | response.status_code != 200:
                # If the number of lines is less than 1000, it means we have reached the last page
                break
            page += 1
    counts()
    uniq()


def fetch_total():
    # this function fetches first and last page of serviceChannels
    # first page tells us the amount of total pages, amount of objects per page
    first_url = "https://api.palvelutietovaranto.suomi.fi/api/v11/ServiceChannel?isVisibleForAll=true&page=1&status=Published"
    # note: "isVisibleForAll" parameter changes the results ALOT
    response = requests.get(first_url)
    response_dict = response.json()
    # last page gives us x amount of objects so the formula is following:
    last_url = "https://api.palvelutietovaranto.suomi.fi/api/v11/ServiceChannel?isVisibleForAll=true&page={}&status=Published".format(
        response_dict['pageCount'])
    last_response = requests.get(last_url)
    last_dict = last_response.json()
    for count, obj in enumerate(last_dict['itemList']):
        pass
    # amount of pages * pagesize + amount of objects on last page = total count of results
    print("Total number of objects in ServiceChannels: " +
          str(response_dict['pageCount'] * 1000 + count))


def fetch_details():
    # mainly using this for debugging
    uid = "e3658c00-02c9-4fd4-8062-f89c9e9dfeb3"
    url = "https://api.palvelutietovaranto.suomi.fi/api/v11/ServiceChannel/{}".format(
        uid)
    response = requests.get(url)
    data = response.json()
    with open("details.xlsx", "w") as file:
        for x in data:
            print(x)

main()
# fetch_details()
# fetch_total()
