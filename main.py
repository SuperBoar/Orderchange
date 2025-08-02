from services.order_service import OrderService
from utils.validators import validate_int_input, validate_yes_no, validate_choice

class OrderChange:
    """
    订单变更主类，处理用户交互和调用服务层
    """

    def __init__(self):
        self.order_service = OrderService()

    def main(self):
        """主交互界面"""
        print("=" * 40)
        print("租赁管理系统 - 场景处理器")
        print("=" * 40)

        # 登录系统
        print("\n正在登录系统...")
        if not self.order_service.login_systems():
            print("系统登录失败，请检查网络连接或联系管理员！")
            return

        try:
            order_id = input("\n请录入订单id：")

            while True:
                print("\n请选择场景类型:")
                print("a: 账单逾期场景")
                print("b: 归还场景")
                print("c: 租转售场景")
                print("d: 租用中")
                print("e: 恢复待发货状态（只用于首期+保证金支付，其他未支付订单）")
                print("q: 退出系统")

                choice = input("\n请输入选项: ").lower()

                try:
                    if choice == 'a':
                        self._handle_scenario_a(order_id)
                    elif choice == 'b':
                        self._handle_scenario_b(order_id)
                    elif choice == 'c':
                        self._handle_scenario_c(order_id)
                    elif choice == 'd':
                        self._handle_scenario_d(order_id)
                    elif choice == 'e':
                        self._handle_scenario_e(order_id)
                    elif choice == 'q':
                        print("\n感谢使用，系统退出！")
                        break
                    else:
                        print("无效选项，请重新输入！")
                except Exception as e:
                    print(f"\n执行出错：{e}")
                    
        except KeyboardInterrupt:
            print("\n\n程序被用户中断退出！")
        except Exception as e:
            print(f"\n程序运行出错：{e}")
        finally:
            # 程序退出时关闭数据库连接
            self.order_service.order_repository.close_connection()

    def _handle_scenario_a(self, order_id):
        """处理账单逾期场景"""
        print("\n===== 逾期场景 =====")
        term = validate_int_input("请输入账单期数: ")
        overdue_days = validate_int_input("请输入逾期天数: ")

        print("正在执行操作...")
        result = self.order_service.execute_scenario_a(order_id, term, overdue_days)
        if result:
            print("数据修改成功！")
        else:
            print("数据修改失败！")

    def _handle_scenario_b(self, order_id):
        """处理归还场景"""
        print("\n===== 归还场景 =====")
        return_days = validate_int_input("请输入租期结束前天数(可负数): ")

        print("正在执行操作...")
        result = self.order_service.execute_scenario_b(order_id, return_days)
        if result:
            print("数据修改成功！")
        else:
            print("数据修改失败！")

    def _handle_scenario_c(self, order_id):
        """处理租转售场景"""
        print("\n===== 租转售场景 =====")
        sub_choice = validate_choice("请选择类型 (x: 账单逾期租转售, y: 归还逾期租转售): ", ['x', 'y'])

        if sub_choice == 'x':
            term = validate_int_input("请输入需要逾期的账单期数: ")
            overdue_days = validate_int_input("请输入租转售逾期天数: ")
            
            print("正在执行操作...")
            result = self.order_service.execute_scenario_c_x(order_id, term, overdue_days)
            if result:
                print("数据修改成功！")
            else:
                print("数据修改失败！")

        elif sub_choice == 'y':
            overdue_days = validate_int_input("请输入归还逾期天数: ")
            
            print("正在执行操作...")
            result = self.order_service.execute_scenario_c_y(order_id, overdue_days)
            if result:
                print("数据修改成功！")
            else:
                print("数据修改失败！")

    def _handle_scenario_d(self, order_id):
        """处理租用中场景"""
        print("\n===== 租用中场景 =====")
        modify_choice = validate_yes_no("是否修改账单日时间? (y/n): ")
        
        term = None
        adjust_days = None
        if modify_choice == 'y':
            term = validate_int_input("请输入需要修改的账单期数: ")
            adjust_days = validate_int_input("请输入要调整至账单日前几天天数: ")

        print("正在执行操作...")
        result = self.order_service.execute_scenario_d(
            order_id, 
            modify_bill_date=(modify_choice == 'y'), 
            term=term, 
            adjust_days=adjust_days
        )
        if result:
            print("数据修改成功！")
        else:
            print("数据修改失败！")

    def _handle_scenario_e(self, order_id):
        """处理恢复待发货场景"""
        print("\n===== 租转售恢复租用中场景 =====")
        
        print("正在执行操作...")
        result = self.order_service.execute_scenario_e(order_id)
        if result:
            print("数据修改成功！")
        else:
            print("数据修改失败！")


if __name__ == "__main__":
    app = OrderChange()
    app.main()