import cx_Oracle
import pandas as pd
import ParamUtil
import sys
from LoggerTools import log

# python使用cx_Oracle直联oracle数据库
# 下为具体配置流程：（注意版本号）
# https://blog.csdn.net/qq_38135191/article/details/123775892

def getETLinfo(etlJobList):
    conn = cx_Oracle.connect(ParamUtil.ETL_USER, ParamUtil.ETL_PASSWORD, ParamUtil.ETL_URL)
    cursor = conn.cursor()

    jobList = etlJobList.split(",")
    jobStr = ""

    # joblist拼接成jobstr  ['ETL_DW00', 'ETL_DW05'] -> 'ETL_DW00','ETL_DW05',
    if jobList == ['']:
        log.error("ETL状态检查任务错误:未配置ETL_JOB_LIST参数")
    else:
        log.info("ETL状态检查任务开始,当前任务为:" + ParamUtil.ETL_JOB_LIST)
        for item in jobList:
            jobStr = jobStr +"'"+ item + "',"

    # 切片处理去掉最后一个,号
    jobStr = jobStr[:len(jobStr)-1]

    sqlJobInfoALL = """SELECT t1.TASKID
           ,t1.BATCHDATE
           ,decode(t1.status,'0','就绪','1','运行中','2','成功','3','失败','9','外部中断','待执行') as STATUS
           ,t1.STARTTIME
           ,t1.ENDTIME
           ,t2.Y
           ,t2.N
           ,t2.T
           ,CASE WHEN t1.BATCHDATE != TO_CHAR(SYSDATE - 1,'YYYYMMDD') THEN '错误：批次《'||t1.BATCHDATE||'》批次时间异常!!!'
                 WHEN t1.status != '2' THEN '警告：批次《'||t1.BATCHDATE||'》当前状态为-'||decode(t1.status,'0','就绪','1','运行中','2','成功','3','失败','9','外部中断','待执行')
                 WHEN t2.TASKID IS NULL THEN '错误：批次《'||t1.BATCHDATE||'》批次执行数据异常!!!'
                 WHEN t2.N > 0 THEN  '错误：批次《'||t1.BATCHDATE||'》存在'||t2.N||'条失败任务!!!'
                 ELSE '成功' END AS FLAG
        FROM sch_schdulecontrol T1
       LEFT JOIN (SELECT T.TASKID
                         ,COUNT(CASE WHEN T.STATUS='2' THEN T.JOBID END) AS Y
                         ,COUNT(CASE WHEN T.STATUS='3' THEN T.JOBID END) AS N
                         ,COUNT(CASE WHEN T.STATUS='5' THEN T.JOBID END) AS T
                    FROM SCH_TASKSTATUS T
                   WHERE BATCHDATE = TO_CHAR(SYSDATE - 1,'YYYYMMDD')
                   GROUP BY T.TASKID) t2
                      on t1.TASKID =  t2.TASKID
                      WHERE t1.TASKID IN (%(joblist)s)"""

    # sql传参，替换joblist
    sqlJobInfoALL = sqlJobInfoALL % {"joblist":jobStr}

    # cursor.execute(sql)
    # result = cursor.fetchall()
    # print(result)
    try:
        data = pd.read_sql_query(sqlJobInfoALL,conn)
        return data
    except Exception:
        log.error("sql语句异常，连接数据库失败！")
        info = sys.exc_info()
        print(info[0], ":", info[1])
    finally:
        cursor.close()
        conn.close()
