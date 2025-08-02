import os
import configparser
# from common.log import MyLog as Log

proDir = os.path.split(os.path.realpath(__file__))[0]
parDir= os.path.dirname(proDir)
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        # self.log = Log.get_log()
        # self.logger = self.log.get_logger()

        try:
            with open(configPath, 'r', encoding='utf-8-sig') as fd:
                data = fd.read()

            self.cf = configparser.ConfigParser()
            self.cf.read_string(data)  # 直接从字符串读取配置
        except Exception as e:
            # self.logger.error(f"Error reading configuration file: {e}")
            raise

    def get_http(self, httpname):
        value = self.cf.get("HTTP", httpname)
        return value

    def get_db(self):
        # value = self.cf.get("DATABASE", name)
        # return value
        db_config = self.cf.items("DATABASE")
        # 将获取的结果转换为字典形式方便使用
        db_dict = dict(db_config)
        return db_dict

    def get_sql(self, sql):
        value = self.cf.get("SQL", sql)
        return value

if __name__ == '__main__':
    print(ReadConfig().get_db())