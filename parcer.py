import pprint

import pandas as pd
import json
from main import check_person


def parce(_id):
    excel_data = pd.read_excel(f'savedFiles/{_id}diary.xlsx')
    m = [(excel_data[f'Unnamed: {1 + 4 * i}'][5:], excel_data[f'Unnamed: {2 + 4 * i}'][5:], excel_data[f'Unnamed: {3 + 4 * i}'][5:]) for i in range(6)]
    all1 = [tuple([[k if str(k) != 'nan' else "" for k in j] for j in i]) for i in m]
    for i in range(len(all1)):
        all1[i] = (all1[i][0], all1[i][1], list(map(lambda x: "ok" if str(x) != '\n' else '', all1[i][2])))
    m1 = [list(zip(*i)) for i in all1]
    for i in range(len(m1)):
        m1[i] = dict(list(map(lambda x: x[:-1], list(filter(lambda x: all(x), m1[i])))))
    s = {}
    for i in range(1, len(m1) + 1):
        s[str(i)] = m1[i - 1]
    a = check_person(_id)
    with open("database.json") as file:
        sfile = json.load(file)
        if a[1]:
            sfile1 = sfile[str(_id)]
            for i in s.keys():
                sfile1[str(i)] = s[i]
            sfile[str(_id)] = sfile1
        else:
            sfile[str(_id)] = s
    with open("database.json", "w", encoding='utf-8') as file:
        json.dump(sfile, file)
    return


def change_tz(_id, newtz):
    a = check_person(_id)
    with open("database.json") as file:
        sfile = json.load(file)
        if str(_id) in sfile:
            sfile1 = sfile[str(_id)]
            if a[0]:
                sfile1["timez"] = newtz
                sfile[str(_id)] = sfile1
            else:
                sfile[str(_id)] = {"timez": newtz}
        else:
            sfile1 =  {"timez": newtz}
            sfile[str(_id)] = sfile1
    with open("database.json", "w", encoding='utf-8') as file:
        json.dump(sfile, file)
    return


def add_dtime(_id, dtime):
    with open("database.json") as file:
        sfile = json.load(file)
        sfile1 = sfile[str(_id)]
        sfile1["dtime"] = dtime
        sfile[str(_id)] = sfile1
    pprint.pprint(sfile)
    with open("database.json", "w") as file:
        json.dump(sfile, file)
    return
