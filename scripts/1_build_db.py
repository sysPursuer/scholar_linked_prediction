import os
import glob
import json
import sqlite3
import logging
from tqdm import tqdm
import argparse

fmt = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG,format=fmt)


stop_word = ["研究兴趣","experience","教育","背景"]

def get_contents(filename):
    id = os.path.basename(filename).split(".")[0]
    with open(filename,"r",encoding="utf-8") as f:
        original_attributes = f.read().strip()
        preprocessed_attributes = "\n".join([text for text in original_attributes.split("\n") if text not in stop_word])
    return (id,original_attributes,preprocessed_attributes)


def build_db(attribute_dir,save_path,linkednodes_path):
    if os.path.isfile(save_path) :
        raise RuntimeError("%s already exists! not overwriting."%save_path)

    nodeTolinkednodes = None
    if os.path.isfile(linkednodes_path):
        with open(linkednodes_path) as f:
            nodeTolinkednodes = json.load(f)
    if nodeTolinkednodes is not None:
        keys = set(nodeTolinkednodes.keys())
    filepathlist = glob.glob(attribute_dir+"/*")

    logging.info("writing into {}...".format(save_path))
    conn = sqlite3.connect(save_path)
    cursor = conn.cursor()
    cursor.execute("create table scholars (id PRIMARY KEY,original_attributes,attributes,linkednodes);")
    for filename in tqdm(filepathlist):
        id,original_attributes,attributes = get_contents(filename)
        linkednodes=""
        if nodeTolinkednodes is not None and str(id) in keys:
            linkednodes = ",".join([ str(i) for i in nodeTolinkednodes[str(id)] ])
        cursor.execute(
            "insert into scholars values (?,?,?,?)",(id,original_attributes,attributes,linkednodes)
        )
    conn.commit()
    conn.close()
    logging.info("wrrting {} scholars Done!".format(len(filepathlist)))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--attribute_dir',type=str,default="../attribute")
    parser.add_argument("--save_path",type=str,default="./processed/scholars.db")
    parser.add_argument("--linkednodes_path",type=str,default="./processed/nodeTolinkednodes_train.json")

    args = parser.parse_args()
    build_db(args.attribute_dir,args.save_path,args.linkednodes_path)