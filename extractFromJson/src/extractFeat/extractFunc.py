# coding:utf-8
from numpy import mean
from numpy import std
import time
import re

NULL = "null"


def hasIP(sni):
    '''
    :param sni: List类型，server name indicator
    :return: 其中有ip就true
    '''
    p = re.compile("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$")
    for i in sni:
        if p.match(i):
            return True
    return False


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
    :return:packets_length[min,max,mean,std].extend(inter_arrival_time[min,max,mean,std])
    '''
    try:
        packets = sorted(flow["packets"], key=lambda pkt: pkt["ipt"])  # 依据到达时间排序
        packets_length = []
        inter_arrival_time = [0]
        for pkt in packets:
            packets_length.append(pkt['b'])
        for i in range(1, len(packets)):  # 从1开始，因为第一个包的inter-arrival time始终为0
            inter_arrival_time.append(packets[i]["ipt"])
        ret = [min(packets_length), max(packets_length), int(mean(packets_length))
            , int(std(packets_length))
            , min(inter_arrival_time), max(inter_arrival_time), int(mean(inter_arrival_time))
            , int(std(inter_arrival_time))]
        return ret
    except:
        return [NULL, NULL, NULL, NULL, NULL, NULL]


def extractTlsInfo(flow):
    '''
    :param flow: flow是dict类型，tls也是dict类型，sni,cs,c_extentions都是list类型
    :return:flow["cs","cs_len","c_extensions","c_extensions_len","c_key_length" ,"SNIisIP"]
    '''
    ret = []
    # cs
    try:
        ret.append(flow["tls"]["cs"])
    except:
        ret.append(NULL)
    # cs_len
    try:
        if ret[0] != NULL:
            ret.append(len(ret[0]))
        else:
            ret.append(NULL)
    except:
        ret.append(NULL)

    # extensions
    try:
        ret.append(flow["tls"]["c_extensions"])
    except:
        ret.append(NULL)
    # extensions_len
    try:
        if ret[0] != NULL:
            ret.append(len(ret[2]))
        else:
            ret.append(NULL)
    except:
        ret.append(NULL)

    # c_key_len
    try:
        ret.append(flow["tls"]["c_key_length"])
    except:
        ret.append(NULL)

    # SNIisIP
    try:
        sni = flow["tls"]["sni"]
        ret.append(hasIP(sni))
    except:
        ret.append(NULL)

    return ret


def extractCertInfo(flow):
    '''
    提取证书信息
    :param flow:传入数据流，flow是dict类型，tls也是dict类型，s_cert是list
    :return:[certChainLen,issuerLen,expiration,certExtLen,subjectLen,isSubEqualIsu,divition]
    '''
    ret = []
    try:
        cert = flow['tls']['s_cert']
    except:
        return [NULL]*7
    if len(cert)==0:
        return [NULL]*7
    try:
        #证书链长度
        certChainLen = len(cert)
        #第一张证书发行者路径长度
        issuerLen = len(cert[0]['issuer'])
        #第一张证书的有效期
        GMT_FORMAT = "%b %d %H:%M:%S %Y GMT"
        cert_begin = time.mktime(time.strptime(cert[0]["validity_not_before"],GMT_FORMAT))
        cert_end = time.mktime(time.strptime(cert[0]["validity_not_after"],GMT_FORMAT))
        expiration = cert_end - cert_begin
        #第一张证书的扩展数量
        certExtLen = len(cert[0]['extensions'])
        #第一张证书的主题路径长度
        subjectLen = len(cert[0]['subject'])
        #第一张证书的issuer和subject是否相同
        issuerCN, = cert[0]['issuer'][-1].values()
        subjectCN, = cert[0]['subject'][-1].values()
        isSubEqualIsu = (issuerCN==subjectCN)
        #已生效时间/总有效时间
        flow_time = flow["time_start"]
        divition = (flow_time-cert_begin)/(expiration)

        return [certChainLen,issuerLen,expiration,certExtLen,subjectLen,isSubEqualIsu,divition]
    except:
        return [NULL]*7



def extract(flow):
    ret = []

    base_info = extractBaseInfo(flow)
    packets_info = extractPacketsInfo(flow)
    tls_info = extractTlsInfo(flow)
    cert_info = extractCertInfo(flow)

    ret.extend(base_info)
    ret.extend(packets_info)
    ret.extend(tls_info)
    ret.extend(cert_info)
    return ret

