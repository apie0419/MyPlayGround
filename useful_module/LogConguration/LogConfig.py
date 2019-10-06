import logging
import logging.handlers
import os, platform

base_path = os.path.dirname(os.path.abspath(__file__))


class LogConfigurator:

    __error_log_dir = os.path.join(base_path, "../../log/error")
    __common_log_dir = os.path.join(base_path, "../../log/common")
    __format = "%(levelname)-7s - %(asctime)s -%(message)s"
    if platform.system() == "Windows":
        __date_format = "%Y-%m-%d %H:%M:%S"
    else:
        __date_format = "%Y-%m-%d %H:%M:%s"

    @staticmethod
    def initialize_logger():
        try:
            logging.basicConfig(
                level = logging.DEBUG, format = LogConfigurator.__format, datefmt = LogConfigurator.__date_format
            )
            LogConfigurator.__create_dirs_for_log()
            LogConfigurator.__configure_access_log()
            LogConfigurator.__configure_error_log_handler()
            LogConfigurator.__configure_common_log_handler()
        except Exception as e:
            print ("Configure logger failed.")
            print (str(e))

    @staticmethod
    def __create_dirs_for_log():
        for dir in [LogConfigurator.__error_log_dir, LogConfigurator.__common_log_dir]:
            if os.path.exists(dir) is False:
                os.makedirs(dir)

    @staticmethod
    def __configure_access_log():
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    @staticmethod
    def __configure_error_log_handler():
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(LogConfigurator.__error_log_dir, 'error.log'), when='midnight'
        )
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(
                fmt = LogConfigurator.__format, datefmt = LogConfigurator.__date_format
            )
        )
        logging.getLogger().addHandler(handler)

    @staticmethod
    def __configure_common_log_handler():
        handler = logging.handlers.TimedRotatingFileHandler(
            filename = os.path.join(LogConfigurator.__common_log_dir, 'common.log'), when = 'midnight'
        )
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(
            logging.Formatter(
                fmt = LogConfigurator.__format, datefmt = LogConfigurator.__date_format
            )
        )
        logging.getLogger().addHandler(handler)
