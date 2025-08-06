from common.log import MyLog as Log
from config import read_config
from common.request import Request
from utils.public import Public

class LogIn:
    """登录类，处理不同系统的登录操作"""

    def __init__(self):
        """初始化登录类实例"""
        self.request = Request()
        self.ocr = Public()
        self.read_config = read_config.ReadConfig()
        self.log = Log.get_log()
        self.logger = self.log.get_logger()

    def login(self, longin_way, login_info=None):
        """
        Args:
            longin_way (str): 登录方式标识
            login_info (dict, optional): 登录信息

        Returns:
            str or None: GO系统返回token，其他系统返回cookie，失败返回None
        """
        self.logger.info("开始执行登录操作")

        try:
            # 根据登录方式选择请求方法
            method = "POST" if longin_way == "GO_LONGIN_URL" else "POST_FORM"
            url = self.read_config.get_http(longin_way)

            login_response = self.request.web_main(url, method, data=login_info)

        except Exception as e:
            self.logger.error(f"网络请求异常: {e}")
            return None

        # 根据登录方式处理响应
        if longin_way == "GO_LONGIN_URL":
            return self._handle_go_login_response(login_response)
        else:
            return self._handle_java_login_response(login_response)

    def _handle_go_login_response(self, response):
        """
        处理GO系统登录响应
        Args:
            response (dict): 登录响应数据

        Returns:
            str or None: 成功返回token，失败返回None
        """
        if response.get('code') == 0:
            self.logger.info(f"登录成功，响应数据：{response}")
            return response["data"]["token"]
        else:
            self.logger.error(f"登录失败，响应数据：{response}")
            return None

    def _handle_java_login_response(self, response):
        """
        处理Java系统登录响应
        Args:
            response: 登录响应对象

        Returns:
            str: Cookie字符串
        """
        self.logger.info(f"登录成功，响应数据：{response}")

        # 获取Cookie字符串用于后续请求头
        cookie_list = [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
        cookie_header = "; ".join(cookie_list)

        self.logger.info(f"Cookie头信息: {cookie_header}")
        return cookie_header


# if __name__ == '__main__':
#     login_instance = LogIn()
#     login_instance.login(longin_way="JAVA_LONGIN_URL")

