import requests
import pandas


def clear_file():
    # Write a line in file overwriting it completely
    with open("data.txt", "w") as file:
        file.write("")


def write_file(data):
    # Append lines in the file
    with open("data.txt", "a") as file:
        for l in enumerate(data['itemList']):
            file.write(l.__str__()[l.__str__().find("{"):-1]+"\n")


def counts():
    # Count lines in file
    with open("data.txt", "r") as neat_file:
        for count, line in enumerate(neat_file):
            pass
        print("Amount of results: ", count + 1)


def uniq():
    # Check for unique lines in file by inserting every line into a set which only accepts unique values
    test_set = set()
    with open("data.txt", "r") as file:
        for count, line in enumerate(file):
            test_set.add(line)
    with open("data_final.txt", "w") as final_file:
        for count, line in enumerate(test_set):
            final_file.write(line)
    print("Amount of unique results: "+str(test_set.__len__()))


def write_excel():
    # Write contents of data.txt into excel file
    with open("data.txt", "r") as data:
        df = pandas.DataFrame(data)
        df.to_excel('data.xlsx', index=False)


def main():
    code = "P27.1"
    url = "https://api.palvelutietovaranto.suomi.fi/api/v11/Service/serviceClass?uri=http%3A%2F%2Furi.suomi.fi%2Fcodelist%2Fptv%2Fptvserclass2%2Fcode%2F{}".format(
        code)
    page = 1
    while True:
        params = {"page": page}
        response = requests.get(url, params=params)
        data = response.json()

        # Do something with the data here
        write_file(data)
        if len(data['itemList']) < 1000:
            # If the number of lines is less than 1000, it means we have reached the last page
            break
        page += 1
    counts()
    uniq()
    # write_excel()


# clear_file()
main()