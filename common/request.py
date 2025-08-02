import logging

import requests

class Request:
    def send_get(self, url, data = None,headers = None):
        res = requests.get(url=url,data = data, headers=headers).json()
        print(res)
        return res

    def send_post(self, url, data = None, headers = None):
        res = requests.post(url=url, data=data, headers=headers).json()
        print( res)
        return res

    def send_post1(self, url, data, headers = None):
        res = requests.post(url=url, data=data)
        return res

    def send_options(self, url, data, headers = None):
        res = requests.options(url=url, params=data).json()
        return res

    def web_main(self, url, method, data=None, headers = None):

        # 支持的方法列表
        supported_methods = ['GET', 'POST','POST1', 'OPTIONS']

        # 检查 method 是否有效
        if method.upper() not in supported_methods:
            raise ValueError(f"不支持的请求方法：'{method}'. 支持的请求方法： {supported_methods}.")

        # 使用映射来选择合适的方法
        method_to_function = {
            'GET': self.send_get,
            'POST': self.send_post,
            'POST1': self.send_post1,
            'OPTIONS': self.send_options
        }

        try:
            # 根据 method 选择合适的方法并执行
            res = method_to_function[method.upper()](url, data,headers)
        except Exception as e:
            # 异常处理
            logging.error(f"发生错误，错误信息: {e}")
            res = None

        return res

# if __name__ == '__main__':
#     request = Request()
#     request.web_main("http://job.dev.bajiezu.cn/xxl-job-admin/jobinfo/trigger?id=72", "post",
#                      headers={"cookie":"XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d"})
