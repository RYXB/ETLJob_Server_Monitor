from Py2Oracle import getETLinfo
from LoggerTools import log
from DingDingMsg import DD2MSG
import ParamUtil
import time


def etl_status_check():
    log.info("开始检查ETL任务!")
    # 获取当前日期 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # sys_now_hour = time.strftime('%H', time.localtime())
    # sys_now_minute =  time.strftime('%M', time.localtime())
    sys_now_hour = "07"
    sys_now_minute = "00"

    # 当小时数为10以下的且长度为1的转化为2位  eg: 9->09
    if(int(ParamUtil.ETL_TIMING_PUSH_H) < 10 and len(ParamUtil.ETL_TIMING_PUSH_H) == 1):
        ParamUtil.ETL_TIMING_PUSH_H = '0' + ParamUtil.ETL_TIMING_PUSH_H
    # 当分钟数为10以下的且长度为1的转化为2位  eg: 9->09
    if(int(ParamUtil.ETL_TIMING_PUSH_MI) < 10 and len(ParamUtil.ETL_TIMING_PUSH_MI) == 1):
        ParamUtil.ETL_TIMING_PUSH_MI = '0' + ParamUtil.ETL_TIMING_PUSH_MI

    if(sys_now_hour.__eq__(ParamUtil.ETL_TIMING_PUSH_H) and sys_now_minute.__eq__(ParamUtil.ETL_TIMING_PUSH_MI)):
        data = getETLinfo(ParamUtil.ETL_JOB_LIST)
        job_list = ""

        # 遍历配置文件中的任务列表
        for item in ParamUtil.ETL_JOB_LIST.split(','):
            job_list = item + job_list
        # print(job_list)

        # 与oracle调度库中处于上线状态的任务进行对比
        for item in data['TASKID']:
            job_list = job_list.replace(item,'')
        # print(job_list)

        if(len(job_list)>0):
            log.error("错误：没有找到任务批次:"+job_list)
            DD2MSG(str("错误：没有找到任务批次:"+job_list))
        else:
            if(data[data['FLAG'] != "成功"].empty):
                log.info("信息：今日仓库批次执行成功!!")
                DD2MSG(str("信息：今日仓库批次执行成功!!"))
            else:
                for item in data[data['FLAG'] != "成功"][['TASKID','FLAG']].values:
                    DD2MSG(str(item))

    log.info("ETL任务检查完毕!")

if __name__ == '__main__':

    log.info("当前已开启ETL状态检查!")
    if(ParamUtil.ETL_FLAG.__eq__("true")):
        etl_status_check()