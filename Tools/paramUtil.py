import os
import configparser
from LoggerTools import log
import sys

# 读取配置文件
def getConfig(filename, section, option):
    """
    :param filename 文件名称
    :param section: 服务
    :param option: 配置参数
    :return:返回配置信息
    """

    # 获取当前目录路径
    proDir = os.path.split(os.path.dirname(__file__))[0]
    # print(proDir)

    # 拼接路径获取完整路径
    configPath = os.path.join(proDir, filename).replace('\\','/')
    # print(configPath)

    # 创建ConfigParser对象
    conf = configparser.ConfigParser()

    # 读取文件内容
    conf.read(configPath,encoding='UTF-8')
    config = conf.get(section, option)
    return config


# 获取oracle配置信息
try:
    ETL_FLAG = getConfig("config\jobAndStatus2DingDing.ini", 'ORACLE', 'ETL_FLAG')
    ETL_URL = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_URL')
    ETL_USER = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_USER')
    ETL_PASSWORD = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_PASSWORD')
    ETL_DD_TOKEN = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_DD_TOKEN')
    ETL_DD_SECRET = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_DD_SECRET')
    ETL_TIMING_PUSH_H = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_TIMING_PUSH_H')
    ETL_TIMING_PUSH_MI = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_TIMING_PUSH_MI')
    ETL_JOB_LIST = getConfig("config\jobAndStatus2DingDing.ini", "ORACLE", 'ETL_JOB_LIST')

    # print(ETL_FLAG, ETL_URL, ETL_USER, ETL_PASSWORD, ETL_DD_TOKEN, ETL_TIMING_PUSH_H, ETL_TIMING_PUSH_MI, ETL_JOB_LIST)
except Exception as reason:
    log.error("读取配置文件错误，参数初始化失败！")
    info = sys.exc_info()
    print(info[0], ":", info[1])