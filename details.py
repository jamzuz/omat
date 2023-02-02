import requests
import pandas


def process_frame(frame):
    new_frame = dict()
    #  add service names to the new frame
    service_names = dict()
    for name in frame['serviceNames']:
        service_names.update({"name": name['value']})
    new_frame.update({"serviceNames": service_names})
    # add munincipalities to the new frame
    muns = {'munincipalities': []}
    for area in frame['areas']:
        for mun in area['municipalities']:
            muns["munincipalities"].append({"name": mun['name'][0]['value']})
    new_frame.update({"munincipalities": muns})
    # add service classes to the new frame
    service_class = {"serviceClasses": []}
    for cl in frame['serviceClasses']:
        service_class["serviceClasses"].append(
            {"name": cl['name'][2]['value'], "code": cl['code']})
    new_frame.update(service_class)
     # add id to the frame
    new_frame.update({"id": frame['id']})
    # add modified date to the new frame
    new_frame.update({"modified": frame['modified']})
    return new_frame


def package_and_send():
    counter = 0
    total = 0
    guids_list = []
    data_frame = []

    with open("data_final.txt", "r") as file:
        for obj in file:
            if counter == 99:
                # make the parameters for the uids
                guids = ",".join(guids_list)
                # add parameters to the url
                url = "https://api.palvelutietovaranto.suomi.fi/api/v11/Service/list?guids={}".format(
                    guids)
                # send data when we reach the limit(max 100 per request)
                response = requests.get(url)
                # create new dataframe with the data from response.json
                for objects in response.json():
                    data_frame.append(process_frame(objects))
                guids_list.clear()
                counter = 0
                total += 1
                print("adding lines into dataframe, Total frames: "+str(total))
            else:
                guids_list.append(str(obj))
                counter += 1
                total += 1
        # query remaining data
        guids = ",".join(guids_list)
        url = "https://api.palvelutietovaranto.suomi.fi/api/v11/Service/list?guids={}".format(
            guids)
        response = requests.get(url)
        for x in response.json():
            data_frame.append(process_frame(x))
        data = pandas.DataFrame(data_frame)
        print("Writing excel file, this might take awhile....")
        data.to_excel('list_data.xlsx',sheet_name='liikuntapaikka data', index=False)

package_and_send()
