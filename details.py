import requests
import pandas


def process_frame(frame):
    new_frame = dict()
    #  add service names to the new frame
    service_names = dict()
    for name in frame['serviceNames']:
        if name["language"] == "fi":
            service_names.update({"name": name['value']})
    new_frame.update({"serviceNames": service_names})
    # add munincipalities to the new frame
    muns = {'munincipalities': []}
    for area in frame['areas']:
        for mun in area['municipalities']:
            for x in mun['name']:
                if x['language'] == 'fi':
                    muns["munincipalities"].append({"name": x['value']})
    new_frame.update({"munincipalities": muns})
    #  add service descriptions to the new frame
    service_desc = {"serviceDescriptions": []}
    for desc in frame['serviceDescriptions']:
        if desc['type'] == "Description" and desc['language'] == "fi":
            service_desc["serviceDescriptions"].append(
                {"value": desc['value']})
    new_frame.update({"serviceDescriptions": service_desc})
    # add service classes to the new frame
    service_class = {"serviceClasses": []}
    for cl in frame['serviceClasses']:
        for name in cl['name']:
            if name['language'] == 'fi':
                service_class["serviceClasses"].append(
                    {"name": name['value'], "code": cl['code']})
    new_frame.update(service_class)
    # add id to the frame
    new_frame.update({"id": frame['id']})
    # add modified date to the new frame
    new_frame.update({"modified": frame['modified']})
    return new_frame


def process_frame_new(frame):
    new_frame = dict()
    #  add service names to the new frame
    service_names = []
    for name in frame['serviceNames']:
        if name["language"] == "fi":
            service_names.append(name['value'])
    new_frame.update({"serviceNames": service_names})
    # add munincipalities to the new frame
    muns = []
    for area in frame['areas']:
        for mun in area['municipalities']:
            for x in mun['name']:
                if x['language'] == 'fi':
                    muns.append(x['value'])
    new_frame.update({"munincipalities": muns})
    #  add service descriptions to the new frame
    service_desc = []
    for desc in frame['serviceDescriptions']:
        if desc['type'] == "Description" and desc['language'] == "fi":
            service_desc.append(desc['value'])
    new_frame.update({"serviceDescriptions": service_desc})
    # add service classes to the new frame
    # service_class = []
    # for cl in frame['serviceClasses']:
    #     for name in cl['name']:
    #         if name['language'] == 'fi':
    #             service_class.append(
    #                 name['value'])
    # new_frame.update({"serviceClass": service_class})
    # add id to the frame
    new_frame.update({"id": frame['id']})
    # add modified date to the new frame
    new_frame.update({"modified": frame['modified']})
    return new_frame


def package_and_send():
    codes = ["P27", "P27.1"]
    P27 = pandas.DataFrame()
    P271 = pandas.DataFrame()
    for code in codes:
        counter = 0
        total = 0
        guids_list = []
        data_frame = []
        with open(str(code+".txt"), "r") as file:
            for line in file:
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
                        data_frame.append(process_frame_new(objects))
                    guids_list.clear()
                    counter = 0
                    total += 1
                    print("adding lines into dataframe, Total frames: "+str(total))
                else:
                    guids_list.append(line)
                    counter += 1
                    total += 1
        # query remaining data
        guids = ",".join(guids_list)
        url = "https://api.palvelutietovaranto.suomi.fi/api/v11/Service/list?guids={}".format(
            guids)
        response = requests.get(url)
        for x in response.json():
            data_frame.append(process_frame_new(x))
        data = pandas.DataFrame(data_frame)
        if code == "P27":
            P27 = data
        else:
            P271 = data
    print("Writing excel file, this might take awhile....")
    with pandas.ExcelWriter("testi.xlsx") as writer:
        P27.to_excel(writer, sheet_name="P27", index=False)
        P271.to_excel(writer, sheet_name="P27.1", index=False)


package_and_send()
