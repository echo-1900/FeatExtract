# coding: utf-8
from configparser import ConfigParser

import pandas as pd

def combineCsv(filenameList,outputfile):
    df_list = []
    for i in filenameList:
        df_list.append(pd.read_csv(i))
    all_data = pd.concat(df_list,axis=1)
    all_data.to_csv(outputfile,index_label=False)

def combineBegin():
    cfg=ConfigParser()
    cfg.read("../../config/config.txt")
    result_dir = cfg.get("filePath","result_dir")
    outputfile = cfg.get("filename","combineOutput")
    inputfile = cfg.get("filename", "combineInput")
    filenames = [result_dir + i for i in inputfile.split(',')]
    outputfile = result_dir+outputfile
    combineCsv(filenames,outputfile)


if __name__ == '__main__':
    combineBegin()
