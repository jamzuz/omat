
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

