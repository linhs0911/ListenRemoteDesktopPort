from subprocess import check_output
import time
import re
import requests
import json

#宣告一個buffer
netstat_buffer = []

#將初次連線的使用者電腦資訊透過 azure 發送 mail
def http_post(string):
    sendMail_url = "https://prod-08.eastasia.logic.azure.com:443/workflows/7ff83c03d79a47c394c8aa6445b1aea6/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=NArFWNF6ESnVkHEACruNMtZvBY-lddLbzc5vvMv25kc"
    header = {"Content-Type" : "application/json"}
    table_re = re.sub("^ +", "",netstat_buffer[0])
    table_re_split = re.split(" +", table_re,0)
    data = {
        "Server" : table_re_split[1],
        "Host" : table_re_split[2],
        "Protocol" : table_re_split[0]
    }
    jdata = json.dumps(data)
    requests.post(sendMail_url, headers = header, data = jdata)

#使用 netStat 聽取遠端連線 port 的狀態
def load_netstat():
    try:
        #命令提示字元所使用的 netstat 指令
        cmd = "netstat -n|findstr \"3389\""
        netstat_table = check_output(cmd,shell = True).decode('utf-8')
        table = netstat_table.split("\r\n")
        for line in table:
            print (line)
            
            #判斷遠端電腦的 Port 是否為正在連線的狀態
            if("203.145.205.20:13389" and "ESTABLISHED" in line):

                #判斷是否連入的 IP 和 Port 是否已經連線
                if (line in netstat_buffer):
                    print ("existent")
                else:
                    print ("non-existent")
                    netstat_buffer.clear
                    netstat_buffer.append(line)
                    http_post(line)
            else:
                netstat_buffer.clear
    except:
        print ("no connection")
        netstat_buffer.clear

while True:
    load_netstat()
    time.sleep(1)