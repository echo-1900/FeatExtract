# coding: utf-8
import json

def preprocessFlow(flow):
    '''
    :param flow: joy原始抓取到的数据流 ，字符串格式
    :return: 丢弃没有tls字段的，格式化有tls字段的
    '''
    json_flow = json.loads(flow)
    if "tls" not in json_flow:
        return -1
    return json_flow
