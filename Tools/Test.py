from Py2Oracle import getETLinfo
import paramUtil

if __name__ == '__main__':
    data = getETLinfo(paramUtil.ETL_JOB_LIST)
    print(data)