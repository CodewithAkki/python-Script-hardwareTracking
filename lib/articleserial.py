def joinWithArticle(data_list, data_list1):
    newList = list()
    for i in range(0, len(data_list)):
        if data_list1 == [] :
            newList.append(data_list[i])
        if data_list1 == 'None':
            newList.append(data_list[i])
        else:
            newList.append(data_list1[i] + "-" + data_list[i])

    return newList
