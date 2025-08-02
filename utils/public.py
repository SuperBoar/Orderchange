import mysql.connector
from mysql.connector import Error
import configparser
import os
import logging


# 初始化日志器（假设 logger 已存在）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Public:
    def __init__(self):
        self.conn = None
        self.logger = logger

    def sql_db(self):
        """创建数据库链接"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/config.ini')

        if not os.path.exists(config_path):
            self.logger.error("配置文件不存在: %s", config_path)
            return None

        try:
            config.read(config_path, encoding='utf-8')
        except Exception as e:
            self.logger.error("读取配置文件出错: %s", e)
            return None

        required_keys = ['host', 'database', 'user', 'password']
        db_config = {}

        try:
            for key in required_keys:
                db_config[key] = config.get('DATABASE', key)
        except configparser.NoOptionError as e:
            self.logger.error("配置文件缺少必要字段: %s", e)
            return None

        try:
            self.conn = mysql.connector.connect(**db_config)
            # if self.conn.is_connected():
            #     self.logger.info("成功连接到MySQL数据库")
            return self.conn
        except Error as e:
            self.logger.error(f"连接失败: {e}")
            return None

    def close_connection(self):
        """
        关闭数据库连接
        """
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            # self.logger.info("MySQL 数据库连接已关闭")

    def execute_sql_list(self, sql_list):
        """
        执行sql语句列表
        """
        if not isinstance(sql_list, list):
            self.logger.error("输入参数必须是SQL语句列表")
            return False

        if not self.conn or not self.conn.is_connected():
            self.logger.error("数据库连接无效")
            return False

        try:
            with self.conn.cursor() as cursor:
                for sql in sql_list:
                    cursor.execute(sql)
                self.conn.commit()
                self.logger.info("SQL语句执行成功")
                return True
        except Error as e:
            self.logger.error(f"SQL执行报错，错误信息: {e}")
            self.conn.rollback()
            return False

    def is_connected(self):
        """
        检查数据库是否连接
        """
        if self.conn is None:
            return False
        return self.conn.is_connected()

# if __name__ == '__main__':
#     db_manager = Public()
#     # db_manager.sql_db()
#     db_manager.close_connection()