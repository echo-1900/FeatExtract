# coding:utf-8
from numpy import mean

NULL = "null"

def extractBaseInfo(flow):
    '''
    :param flow:flow 都是 dict 对象
    :return:flow[ "num_pkts_in", "num_pkts_out","bytes_in", "bytes_out"]
    '''
    ret = []
    baseInfo = [
        "num_pkts_in", "num_pkts_out",
        "bytes_in", "bytes_out"
    ]
    for feat in baseInfo:
        try:
            ret.append(flow[feat])
        except:
            ret.append(NULL)
    return ret


def extractPacketsInfo(flow):
    '''
    :param flow:flow是dict对象，其中的packets元素必须先转化成list,且每个元素是dict类型
    :return:packets_length[min,max,mean].extend(inter_arrival_time[min,max,mean])
    '''
    try:
        packets = sorted(flow["packets"], key=lambda pkt:pkt["ipt"])#依据到达时间排序
        packets_length = []
        inter_arrival_time = [0]
        for pkt in packets:
            packets_length.append(pkt['b'])
        for i in range(1, len(packets)):#从1开始，因为第一个包的inter-arrival time始终为0
            inter_arrival_time.append(packets[i]["ipt"])
        ret = [min(packets_length),max(packets_length),int(mean(packets_length)),
                min(inter_arrival_time),max(inter_arrival_time),int(mean(inter_arrival_time))]
        return ret
    except:
        return [NULL,NULL,NULL,NULL,NULL,NULL]


def extractTlsInfo(flow):
    '''
    :param flow: flow是dict类型，tls也是dict类型，sni,cs,c_extentions都是list类型
    :return:flow["cs","c_extensions","c_key_length" ,"sni"]
    '''
    tls_info = ["cs","c_extensions","c_key_length" ,"sni"]
    ret = []
    for feat in tls_info:
        try:
            ret.append(flow["tls"][feat])
        except:
            ret.append(NULL)
    return ret


def extract(flow):
    ret = []

    base_info = extractBaseInfo(flow)
    packets_info =extractPacketsInfo(flow)
    tls_info = extractTlsInfo(flow)

    ret.extend(base_info)
    ret.extend(packets_info)
    ret.extend(tls_info)
    return ret