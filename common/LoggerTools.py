import logging
from logging.handlers import TimedRotatingFileHandler


class Log(object):

    STAND = "stand"   # 输出到控制台
    FILE = "file"     # 输出到文件
    ALL = "all"       # 输出到控制台和文件

    def __init__(self, mode=STAND):
        self.LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        self.logger = logging.getLogger()
        self.init(mode)

    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)

    def init(self, mode):
        self.logger.setLevel(logging.DEBUG)

        if mode == "stand":
            # 输出到控制台 ------
            self.stand_mode()
        elif mode == "file":
            # 输出到文件 --------
            self.file_mode()
        elif mode == "all":
            # 输出到控制台和文件
            self.stand_mode()
            self.file_mode()

    def stand_mode(self):
        stand_handler = logging.StreamHandler()
        stand_handler.setLevel(logging.DEBUG)
        stand_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        self.logger.addHandler(stand_handler)

    def file_mode(self):
        '''
        filename：日志文件名的prefix；
        when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
         “S”: Seconds
         “M”: Minutes
         “H”: Hours
         “D”: Days
         “W”: Week day (0=Monday)
         “midnight”: Roll over at midnight
        interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件；
        backupCount: 表示日志文件的保留个数；
        '''
        # 输出到文件 -----------------------------------------------------------
        # 按文件大小输出
        # file_handler = RotatingFileHandler(filename="my1.log", mode='a', maxBytes=1024 * 1024 * 5, backupCount=10, encoding='utf-8')  # 使用RotatingFileHandler类，滚动备份日志
        # 按时间输出
        file_handler = TimedRotatingFileHandler(filename="my.log", when="D", interval=1, backupCount=10,
                                                encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        self.logger.addHandler(file_handler)

log = Log(mode=Log.STAND)

