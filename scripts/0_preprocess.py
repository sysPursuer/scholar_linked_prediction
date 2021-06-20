import pandas as pd
import json
import os

#将结点对格式转为十字链表格式
def csv2json(filename):
    if not os.path.isfile(filename):
        print("{} not exists!".format(filename))
        return None
    df = pd.read_csv(filename,header=None)
    nodeTolinkednodes = {}
    keys = set()

    grouped0 = df.groupby(0)
    grouped1 = df.groupby(1)
    for node in grouped0.groups.keys():
        if node not in keys:
            nodeTolinkednodes[node] = []
            keys.add(node)
        nodeTolinkednodes[node] += list(grouped0.get_group(node)[1])

    for node in grouped1.groups.keys():
        if node not in keys:
            nodeTolinkednodes[node]=[]
            keys.add(node)
        nodeTolinkednodes[node] += list(grouped1.get_group(node)[0])

    with open("./processed/nodeTolinkednodes_train.json","a+") as f:
        json.dump(nodeTolinkednodes,f)

    return nodeTolinkednodes


if __name__=="__main__":
    csv2json(r"D:\2021-2022\contests\2nd ChineseCSCW Cup\SCHOLAT Link Prediction\train.csv")
