import requests
import pandas

def package_and_send():
    with open("data_final.txt","r") as file:
        counter = 0
        data = []
        for count, line in enumerate(file):
            if counter == 99:
                # send data when we reach the limit(max 100 per request)
                print(data)
                # write results in excel?

                # clear data and counter
                data.clear()
                counter = 0
            else:
                data.append(line.split("'")[3])
                counter += 1
        #send remaining data 

package_and_send()