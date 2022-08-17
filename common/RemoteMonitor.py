import sys
import ParamUtil
import paramiko
import re
from LoggerTools import log
import pandas as pd
from DingDingMsg import DD2MSG

hostname = ParamUtil.SERVER_IP
port = ParamUtil.SERVER_PORT
username = ParamUtil.SERVER_USER
password = ParamUtil.SERVER_PASSWORD


def ssh_exec(command):
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
内存监控
"""
def mem_info():
    result = ssh_exec('cat /proc/meminfo')
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
    DD2MSG("内存状态检测:"+"\n"+"可用内存:"+ str("%.2f" % (int(MemFree)/1024/1024)) +"GB" +"\n"+"内存利用率："+str("%.2f" % Rate_Mem)+"%")


""" 
磁盘空间监控
"""
def disk_stat():
    # 将查询结果转为pandas.DF
    result = str(ssh_exec('df -a'))
    data = result.strip().split('\\n')
    data.pop(0)

    rdd = []
    #将一列字符串进行切分
    for i in range(0,len(data)-1):
        rdd.append(tuple(filter(None,data[i].strip().replace('-','0').replace(' ', '*').split('*'))))

    # 格式化DataFrame
    rs = pd.DataFrame(rdd,columns=['Filesystem','1K-blocks','Used','Available','Use%','Mounted on'])

    # 磁盘使用率=(Used列数据之和)/(1K-blocks列数据之和)
    used_sum = rs["Used"].astype("int").sum()
    total_sum = rs["1K-blocks"].astype("int").sum()
    available=rs["Available"].astype("int").sum()
    disk_rate = (used_sum/total_sum) * 100
    DD2MSG("磁盘状态检测:"+"\n"+"可用磁盘:"+ str("%.2f" % (available/1024/1024)) +"GB" +"\n"+"磁盘使用率:"+str("%.2f" % disk_rate) + "%")

def check_server_status():
    mem_info()
    disk_stat()
