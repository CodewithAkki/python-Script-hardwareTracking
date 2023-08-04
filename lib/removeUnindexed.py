def removeSerial(data_list, index):
    new_list = list()
    length = len(data_list)
    if length > 1:
        for deleteSerial in range(0, length):
            if deleteSerial not in index:
                data_list[deleteSerial] = " "
        for i in data_list:
            if i:
                new_list.append(i)
        return new_list
    return data_list
