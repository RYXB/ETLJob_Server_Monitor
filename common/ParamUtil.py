import os
import configparser
from common.LoggerTools import log
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


configFilePath = "config\jobAndStatus2DingDing.ini"
# 获取oracle配置信息
try:
    ETL_FLAG = getConfig(configFilePath, 'ORACLE', 'ETL_FLAG')
    ETL_URL = getConfig(configFilePath, "ORACLE", 'ETL_URL')
    ETL_DRIVER = getConfig(configFilePath, "ORACLE", 'ETL_DRIVER')
    ETL_USER = getConfig(configFilePath, "ORACLE", 'ETL_USER')
    ETL_PASSWORD = getConfig(configFilePath, "ORACLE", 'ETL_PASSWORD')
    ETL_DD_TOKEN = getConfig(configFilePath, "ORACLE", 'ETL_DD_TOKEN')
    ETL_DD_SECRET = getConfig(configFilePath, "ORACLE", 'ETL_DD_SECRET')
    ETL_TIMING_PUSH_H = getConfig(configFilePath, "ORACLE", 'ETL_TIMING_PUSH_H')
    ETL_TIMING_PUSH_MI = getConfig(configFilePath, "ORACLE", 'ETL_TIMING_PUSH_MI')
    ETL_JOB_LIST = getConfig(configFilePath, "ORACLE", 'ETL_JOB_LIST')

    CHECK_FLAG = getConfig(configFilePath, "SERVER", 'CHECK_FLAG')
    CHECK_SERVER_H = getConfig(configFilePath, "SERVER", 'CHECK_SERVER_H')
    CHECK_SERVER_MI = getConfig(configFilePath, "SERVER", 'CHECK_SERVER_MI')
    SERVER_IP = getConfig(configFilePath, "SERVER", 'SERVER_IP')
    SERVER_PORT = getConfig(configFilePath, "SERVER", 'SERVER_PORT')
    SERVER_USER = getConfig(configFilePath, "SERVER", 'SERVER_USER')
    SERVER_PASSWORD = getConfig(configFilePath, "SERVER", 'SERVER_PASSWORD')

    # print(ETL_FLAG, ETL_URL, ETL_USER, ETL_PASSWORD, ETL_DD_TOKEN, ETL_DD_SECRET, ETL_TIMING_PUSH_H, ETL_TIMING_PUSH_MI, ETL_JOB_LIST)
except Exception as reason:
    log.error("读取配置文件错误，参数初始化失败！")
    info = sys.exc_info()
    print(info[0], ":", info[1])