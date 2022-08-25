import common.ParamUtil as ParamUtil
from common.LoggerTools import log
from common.RemoteMonitor import check_server_status
from common.ETLMonitor import etl_status_check
from common.DingDingMsg import DD2MSG

if __name__ == '__main__':

    log.info("当前已开启ETL状态检查!")
    if(ParamUtil.ETL_FLAG.__eq__("true")):
        etl_status_check()

    log.info("当前已开启服务器状态检查!")
    if(ParamUtil.CHECK_FLAG.__eq__("true")):
        check_server_status()