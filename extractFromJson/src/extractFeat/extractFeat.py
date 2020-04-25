# coding: utf-8
from configparser import ConfigParser
import csv
from extractFunc import *
from preprocessFlowFunc import *

def extractBegin():
    cfg=ConfigParser()
    cfg.read("../../config/config.txt")
    joy_file_dir = cfg.get("filePath","joy_output_dir")
    result_dir = cfg.get("filePath","result_dir")
    input_file_name = cfg.get("filename","extractInput")
    output_file_name = cfg.get("filename", "extractOutput")


    with open(result_dir+output_file_name,'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "num_pkts_in", "num_pkts_out","bytes_in", "bytes_out"
            ,"min_packets_len","max_packets_len","mean_packets_len","std_packets_len"
            ,"min_ipt","max_ipt","mean_ipt","std_ipt"
            ,"cs","cs_len","c_extensions","c_extensions_len","c_key_length" ,"SNIisIP"
                         ])
        with open(joy_file_dir+input_file_name,'r') as f:
            for line in f.readlines()[1:]:
                flow = preprocessFlow(line)
                if flow == -1:#不包含tls流
                    continue
                features = extract(flow)
                writer.writerow(features)

if __name__ == '__main__':
    extractBegin()