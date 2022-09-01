import sys
import common.ParamUtil as ParamUtil
import paramiko
import re
from common.LoggerTools import log
import pandas as pd
from common.DingDingMsg import DD2MSG
import logging


logging.getLogger("paramiko").setLevel(logging.ERROR)

"""
建立SSH连接，执行shell命令语句
"""
def ssh_exec(hostname,port,username,password,command):
    try:
        ssh = paramiko.SSHClient()  # 创建SSH对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        ssh.connect(hostname=hostname, port=int(port), username=username, password=password)  # 连接服务器

        stdin, stdout, stderr = ssh.exec_command(command)  # 执行命令并获取命令结果
        # stdin为输入的命令
        # stdout为命令返回的结果
        # stderr为命令错误时返回的结果
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        return result
    except Exception as r:
        print(r)
        log.error("SSH连接未建立成功！，请检查配置文件是否正确！")
        sys.exit()
    finally:
        ssh.close()  # 关闭连接
        log.info("SSH连接关闭！")

"""
获取主机名
"""
def hostname_info(hostname,port,username,password):
    result = ssh_exec(hostname,port,username,password,'hostname')
    res = str(result)[2:][:-3]
    return res


"""
内存监控
"""
def mem_info(hostname,port,username,password):
    result = ssh_exec(hostname,port,username,password,'cat /proc/meminfo')
    mem_values = re.findall("(\d+)\ kB", str(result))
    MemTotal = mem_values[0]
    MemFree = mem_values[1]
    Buffers = mem_values[3]
    Cached = mem_values[4]
    # SwapTotal = mem_values[14]
    # SwapFree = mem_values[15]
    # if int(SwapTotal) == 0:
    #     DD2MSG("交换内存总共为：0")
    # else:
    #     Rate_Swap = 100 - 100 * int(SwapFree) / float(SwapTotal)
    #     DD2MSG("交换内存利用率："+Rate_Swap)
    Free_Mem = int(MemFree) + int(Buffers) + int(Cached)
    Used_Mem = int(MemTotal) - Free_Mem
    Rate_Mem = 100 * Used_Mem / float(MemTotal)
    # DD2MSG("内存状态检测:"+"\n"+"可用内存:"+ str("%.2f" % (int(MemFree)/1024/1024)) +"GB" +"\n"+"内存利用率："+str("%.2f" % Rate_Mem)+"%")
    return (MemFree,Rate_Mem)

""" 
磁盘空间监控
"""
def disk_info(hostname,port,username,password):
    # 将查询结果转为pandas.DF
    result = str(ssh_exec(hostname,port,username,password,'df -a'))
    data = result.strip().split('\\n')
    data.pop(0)

    rdd = []
    #将一列字符串进行切分
    for i in range(0,len(data)-1):
        rdd.append(tuple(filter(None,data[i].strip().replace('-','0').replace(' ', '*').split('*'))))

    # 格式化DataFrame
    rs = pd.DataFrame(rdd,columns=['Filesystem','1K-blocks','Used','Available','Use%','Mounted on'])

    # 磁盘使用率=(Used列数据之和)/(1K-blocks列数据之和)
    used_sum = rs["Used"].astype("int64").sum()
    total_sum = rs["1K-blocks"].astype("int64").sum()
    available=rs["Available"].astype("int64").sum()
    disk_rate = (used_sum/total_sum) * 100
    # DD2MSG("磁盘状态检测:"+"\n"+"可用磁盘:"+ str("%.2f" % (available/1024/1024)) +"GB" +"\n"+"磁盘使用率:"+str("%.2f" % disk_rate) + "%")
    return (available,disk_rate)

# 整合mem_info和disk_info方法，并输出至钉钉
def mode_log_info(hostname, port, username, password):

    # 获取host、memory、disk的信息
    servername = hostname_info(hostname, port, username, password)
    mem = mem_info(hostname, port, username, password)
    disk = disk_info(hostname, port, username, password)

    MemFree = mem[0]
    Rate_Mem = mem[1]

    available = disk[0]
    disk_rate = disk[1]

    DD2MSG("服务器"+servername+"\n"+" 内存状态检测:"+"\n"+"可用内存:"+ str("%.2f" % (int(MemFree)/1024/1024)) +"GB" +"\t"+"内存利用率："+str("%.2f" % Rate_Mem)+"%" +"\n"
           +"磁盘状态检测:"+"\n"+"可用磁盘:"+ str("%.2f" % (available/1024/1024)) +"GB" +"\t"+"磁盘使用率:"+str("%.2f" % disk_rate) + "%")

# 将任务配置中多台服务器进行分割检测
def check_server_status():
    log.info("开始服务器状态检查任务!")
    # 获取当前日期 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # sys_now_hour = time.strftime('%H', time.localtime())
    # sys_now_minute =  time.strftime('%M', time.localtime())
    sys_now_hour = "07"
    sys_now_minute = "00"

    hour_list = ParamUtil.CHECK_SERVER_H.split(",")
    minutes_list = ParamUtil.CHECK_SERVER_MI.split(",")

    if (hour_list.__contains__(sys_now_hour) and minutes_list.__contains__(sys_now_minute)):
        hostname = ParamUtil.SERVER_IP.split(",")
        port = ParamUtil.SERVER_PORT.split(",")
        username = ParamUtil.SERVER_USER.split(",")
        password = ParamUtil.SERVER_PASSWORD.split(",")

        hostnameStr = ""
        portInt = ""
        usernameStr = ""
        passwordStr = ""

        # joblist拼接成jobstr  ['ETL_DW00', 'ETL_DW05'] -> 'ETL_DW00','ETL_DW05',
        if hostname == [''] or port == [''] or username == [''] or password == ['']:
            log.error("服务器状态检查任务错误:参数配置异常")
        else:
            log.info("服务器状态检查任务开始,当前服务器为:" + ParamUtil.SERVER_IP)
            for item in hostname:
                hostnameStr = hostnameStr + item + ","
            for item in port:
                portInt = portInt + item + ","
            for item in username:
                usernameStr = usernameStr + item + ","
            for item in password:
                passwordStr = passwordStr + item + ","

        # 切片处理去掉最后一个,号
        hostnameStr = hostnameStr[:len(hostnameStr) - 1].split(',')
        portInt = portInt[:len(portInt) - 1].split(',')
        usernameStr = usernameStr[:len(usernameStr) - 1].split(',')
        passwordStr = passwordStr[:len(passwordStr) - 1].split(',')

        # 调用 mode_log_info(hostname, port, username, password)检测服务器状态
        for (hostname, port, username, password) in zip(hostnameStr, portInt, usernameStr, passwordStr):
            mode_log_info(hostname, port, username, password)

    else:
        log.info("服务器状态检查任务未到时间!")
    log.info("服务器状态检查任务检查完毕!")
