def make_unique(data_list):
    for i in range(0, len(data_list) - 2):
        if data_list[i] == data_list[i + 1]:
            data_list.pop(i + 1)