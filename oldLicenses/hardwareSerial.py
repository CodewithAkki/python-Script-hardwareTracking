from fileVariables import old_hw_log_path
from lib.listToString import listToString
from lib.orderedListUnique import make_unique
from lib.removeUnindexed import removeSerial
from lib.articleserial import joinWithArticle

data = dict()
index = list()



def hardwareSerialNumber():
    try:
        log_file = open(old_hw_log_path, 'r')
        log_lines = log_file.readlines()
        count = -1
        data["Hardware"] = list()
        data['Serial'] = list()
        data['Article'] = list()
        for i in range(5, len(log_lines) + 1):
            try:
                line = log_lines[i].strip().split(':')
                if ['\n'] == line:
                    continue
                if "Hardware" in line:
                    if 'Hardware' in data.keys():
                        for x in line[1:]:
                            data["Hardware"].append(x.strip())
                            count = count + 1
                            index.append(count)

                    else:
                        data[line[0].strip()] = [x.strip() for x in line[1:]]
                        count = count + 1
                        index.append(count)
                if "Serial number" in line:
                    if 'Serial' in data.keys():
                        for x in line[1:]:
                            data["Serial"].append(x.strip())
                            data["Article"].append('None')
                    else:
                        data[line[0].strip()] = [" " for x in line[1:]]
                if "Serial" in line:
                    if "100" not in line[1:]:
                        if 'Serial' in data.keys():
                            for x in line[1:]:
                                data["Serial"].append(x.strip())
                        else:
                            data[line[0].strip()] = [x.strip() for x in line[1:]]

                if "Article" in line:
                    if 'Article' in data.keys():
                        for x in line[1:]:
                            data["Article"].append(x.strip())
                    else:
                        data[line[0].strip()] = [x.strip() for x in line[1:]]
                if "Licenses" in line:
                    # print(data)
                    i += 1
                    line = log_lines[i].strip().split(':')
                    # print(line)
                    if len(line) == 1 and '' in line:
                        if len(data["Hardware"]) == len(data["Serial"]) == len(data["Article"]):
                            if data["Hardware"]:
                                data["Hardware"].pop()
                            if data["Serial"]:
                                data["Serial"].pop()
                            if data["Article"]:
                                data["Article"].pop()
                        else:
                            if data["Serial"]:
                                data["Serial"].pop()
                            if data["Article"]:
                                data["Article"].pop()

            except IndexError:
                continue

        log_file.close()
        print(data)
        data["Serial"] = removeSerial(data["Serial"], index)
        data["Serial"] = make_unique(data["Serial"])
        data["Article"] = removeSerial(data["Article"], index)
        #data["Article"] = make_unique(data["Article"])
        print(data["Article"])
        data["serials"] = joinWithArticle(data['Serial'], data["Article"])
        data['serials'] = listToString(data['serials'])
        data['Hardware'] = listToString(data['Hardware'])
        del data['Article']
        del data['Serial']
        # print(data)
    except FileNotFoundError:
        print("log:>> File not found on : ",old_hw_log_path)
