# coding: utf-8
from configparser import ConfigParser

from pandas import read_csv
import csv
import json

def onehotEncode(filename, fieldName):
    '''
    用于处理csv文件中某一列是list且需要
    对list的中的元素进行独热编码的情形，
    如ciphersuite和extensions
    :param fieldName: 成员为list的列的列名
    :param filename: csv文件文件名
    :return: fieldName的所有出现值，编码好的值
    '''
    encoded_value = []
    all_possible_value = set()
    csvFile = read_csv(filename)
    allList = csvFile[fieldName]
    for i in allList.tolist():#统计所有的可能值
        try:#针对i中元素是字符串的情况，cs
            for value in json.loads(i.replace("\'","\"")):
                all_possible_value.add(value)
        except:#针对i中元素是dict的情况，e_extensions
            try:
                for value in json.loads(i.replace("\'","\"")):
                    extension_name, = value
                    all_possible_value.add(extension_name)
            except:
                pass#针对无cs


    all_possible_value = list(all_possible_value)
    len_ = len(all_possible_value)
    for flow_feature_list in allList.tolist():#对所有值编码
        tmp = [0] * len_
        if isinstance(flow_feature_list,float):#针对值无cs的情况
            encoded_value.append([0] * len_)
        else:
            for index in range(len_):
                if all_possible_value[index] in flow_feature_list:
                    tmp[index] = 1
            encoded_value.append(tmp)
    return all_possible_value,encoded_value



def onehotBegin():
    '''
    将result下初步提取的csv文件中的cs和extensions进行独热编码
    :return:
    '''
    cfg=ConfigParser()
    cfg.read("../../config/config.txt")
    result_dir = cfg.get("filePath","result_dir")
    input_file_name = cfg.get("filename","onehotInput")
    fieldNamesList = cfg.get("onehotfield", "onehotfieldname").split(",")
    for field in fieldNamesList:
        with open(result_dir+"encoded"+field+".csv","w",newline='') as f:
            all_possible_value,encodedvalue = onehotEncode(result_dir+input_file_name,field)
            writer = csv.writer(f)
            writer.writerow(all_possible_value)
            for row in encodedvalue:
                writer.writerow(row)

if __name__ == '__main__':
    onehotBegin()