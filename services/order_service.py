from repositories.order_repository import OrderRepository
from common.request import Request
from common.longin import LogIn
from config import read_config
from time import sleep


class OrderService:
    """
    订单服务类，处理各种订单场景的业务逻辑
    """

    def __init__(self):
        self.read_config = read_config.ReadConfig()
        self.order_repository = OrderRepository()
        self.request = Request()
        self.login = LogIn()
        self.go_token = None
        self.java_cookie = None

    def login_systems(self):
        """
        登录到各个系统
        """
        self.go_token = self.login.login(longin_way="GO_LONGIN_URL")
        self.java_cookie = self.login.login(longin_way="JAVA_LONGIN_URL")
        return self.go_token is not None and self.java_cookie is not None

    def execute_scenario_a(self, order_id, term, overdue_days):
        """
        账单逾期场景处理
        """
        # 执行SQL
        result = self.order_repository.execute_scenario_a_sql(order_id, term, overdue_days)

        # 检查SQL执行结果，只有执行成功才触发接口
        if not result:
            raise Exception("SQL执行失败，请检查日志!")

        # 触发接口
        self.request.web_main(
            self.read_config.get_http("GO_URL1"), 
            "get", 
            headers={"Auth-Token": self.go_token}
        )

        return result

    def execute_scenario_b(self, order_id, return_days):
        """
        归还场景处理
        """
        # 执行SQL
        result = self.order_repository.execute_scenario_b_sql(order_id, return_days)
        # 检查SQL执行结果，只有执行成功才触发接口
        if not result:
            raise Exception("SQL执行失败，请检查日志!")

        # 触发接口
        self.request.web_main(
            self.read_config.get_http("GO_URL2"), 
            "get", 
            headers={"Auth-Token": self.go_token}
        )
        
        if return_days < 0:
            self.request.web_main(
                self.read_config.get_http("GO_URL3"), 
                "get", 
                headers={"Auth-Token": self.go_token}
            )

        return result

    def execute_scenario_c_x(self, order_id, term, overdue_days):
        """
        账单逾期租转售场景处理
        """
        if overdue_days <= 7:
            raise Exception("逾期天数较小，不满足租转售逻辑，请重新输入逾期天数大于7天")

        # 执行SQL
        result = self.order_repository.execute_scenario_c_x_sql(order_id, term, overdue_days)
        
        # 检查SQL执行结果，只有执行成功才触发接口
        if not result:
            raise Exception("SQL执行失败，请检查日志!")

        # 触发接口
        self.request.web_main(
            self.read_config.get_http("GO_URL1"), 
            "get", 
            headers={"Auth-Token": self.go_token}
        )
        sleep(1)
        self.request.web_main(
            self.read_config.get_http("JAVA_URL1"), 
            "post", 
            headers={"cookie": self.java_cookie}
        )

        return result

    def execute_scenario_c_y(self, order_id, overdue_days):
        """
        归还逾期租转售场景处理
        """
        if overdue_days < 7:
            raise Exception("逾期天数较小，不满足租转售逻辑，请重新输入逾期天数大于等于7天")

        # 执行SQL
        result = self.order_repository.execute_scenario_c_y_sql(order_id, overdue_days)
        
        # 检查SQL执行结果，只有执行成功才触发接口
        if not result:
            raise Exception("SQL执行失败，请检查日志!")

        # 触发接口
        self.request.web_main(
            self.read_config.get_http("GO_URL2"), 
            "get", 
            headers={"Auth-Token": self.go_token}
        )
        sleep(1)
        self.request.web_main(
            self.read_config.get_http("GO_URL3"), 
            "get", 
            headers={"Auth-Token": self.go_token}
        )
        sleep(1)
        self.request.web_main(
            self.read_config.get_http("JAVA_URL2"), 
            "post", 
            headers={"cookie": self.java_cookie}
        )

        return result

    def execute_scenario_d(self, order_id, modify_bill_date=False, term=None, adjust_days=None):
        """
        租用中场景处理
        """
        # 执行SQL
        result = self.order_repository.execute_scenario_d_sql(
            order_id, 
            modify_bill_date=modify_bill_date, 
            term=term, 
            adjust_days=adjust_days
        )
        
        return result

    def execute_scenario_e(self, order_id, paid_deposit=False):
        """
        恢复待发货场景处理
        
        Args:
            order_id (str): 订单ID
            paid_deposit (bool): 是否已支付履约保证金，默认为False
                True: 已支付履约保证金
                False: 未支付履约保证金
        """
        # 执行SQL
        result = self.order_repository.execute_scenario_e_sql(order_id, paid_deposit)
        return result

    def execute_scenario_f(self):
        """
        生成代扣参数
        """
        self.request.web_main(
            self.read_config.get_http("JAVA_URL3"),
            "post",
            headers={"cookie": self.java_cookie}
        )