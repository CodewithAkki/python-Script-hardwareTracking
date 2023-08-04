def listToString(data_list):
    str_values = str()
    for i in data_list:
        str_value = ''.join(i)
        if str_values != '':
            str_values = str_values + "," + str_value
        else:
            str_values = str_value
    return str_values.strip()


def remove_licenses(data_list, index):
    newList = dict()
    for deleteSerial in index:
        newList[deleteSerial] = data_list[deleteSerial]
    return newList
