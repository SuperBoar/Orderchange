from utils.public import Public


class OrderRepository:
    """
    订单数据访问类，处理订单相关的数据库操作
    """

    def __init__(self):
        self.db_manager = Public()

    def connect_database(self):
        """
        连接数据库
        
        Returns:
            bool: 连接是否成功
        """
        # 如果已经连接，则直接返回True
        if self.db_manager.is_connected():
            return True
            
        # 如果未连接，则尝试连接
        if not self.db_manager.conn:
            connection_result = self.db_manager.sql_db()
            return connection_result is not None
        return True

    def close_connection(self):
        """
        关闭数据库连接
        """
        self.db_manager.close_connection()

    def _ensure_connection(self):
        """确保数据库连接有效"""
        if not self.db_manager.is_connected():
            self.db_manager.logger.info("尝试重新连接数据库...")
            connection_result = self.db_manager.sql_db()
            if connection_result is None:
                self.db_manager.logger.error("数据库重连失败！")
                return False
            self.db_manager.logger.info("数据库重连成功！")
            return True
        self.db_manager.logger.info("数据库连接正常。")
        return True

    def execute_scenario_a_sql(self, order_id, term, overdue_days):
        """执行账单逾期场景的SQL语句"""
        sql_list = [
            f"update bajiezu.`order` set order_status = '50', sub_status = '50' where order_id = '{order_id}'",
            f"update bajiezu.`order_bill` set `status` = '10' where order_id = '{order_id}' and now_lease_term < {term}",
            f"update bajiezu.`order_bill` set `status` = '0' where order_id = '{order_id}' and now_lease_term >= {term}",
            f"UPDATE `bajiezu`.`order_bill` SET `bill_due_date` = CURDATE() - INTERVAL {overdue_days} DAY "
            f"WHERE order_id = '{order_id}' and now_lease_term = {term}"
        ]
        return self.db_manager.execute_sql_list(sql_list)

    def execute_scenario_b_sql(self, order_id, return_days):
        """执行归还场景的SQL语句"""
        sql_list = [
            f"update bajiezu.`order` set order_status = 50, sub_status = 50 where order_id = '{order_id}'",
            f"update bajiezu.`order_bill` set `status` = '10' where order_id = '{order_id}'",
            f"update order_prepayment set balance = amount, `status`=10 WHERE order_id = '{order_id}'",
            f"update bajiezu.order_info set rent_start_time = DATE_SUB(rent_start_time, INTERVAL 1 YEAR),"
            f"rent_end_time = CURDATE() + INTERVAL {return_days} DAY WHERE order_id = '{order_id}'"
        ]
        return self.db_manager.execute_sql_list(sql_list)

    def execute_scenario_c_x_sql(self, order_id, term, overdue_days):
        """执行账单逾期租转售场景的SQL语句"""
        sql_list = [
            f"update bajiezu.`order` set order_status = '50', sub_status = '50' where order_id = '{order_id}'",
            f"update bajiezu.`order_bill` set `status` = '10' where order_id = '{order_id}' and now_lease_term < {term}",
            f"UPDATE `bajiezu`.`order_bill` SET `status` = '0',`bill_due_date` = CURDATE() - INTERVAL {overdue_days + 7} DAY "
            f"WHERE order_id = '{order_id}' and now_lease_term = {term}",
            f"update bajiezu.order_info set rent_start_time = DATE_SUB(rent_start_time, INTERVAL 1 YEAR),"
            f"rent_end_time = CURDATE() - INTERVAL {overdue_days} DAY WHERE order_id ='{order_id}'"
        ]
        return self.db_manager.execute_sql_list(sql_list)

    def execute_scenario_c_y_sql(self, order_id, overdue_days):
        """执行归还逾期租转售场景的SQL语句"""
        sql_list = [
            f"update bajiezu.`order` set order_status = 50, sub_status = 50 where order_id = '{order_id}'",
            f"update bajiezu.`order_bill` set `status` = '10' where order_id = '{order_id}'",
            f"update order_prepayment set balance = amount, `status`=10 WHERE order_id = '{order_id}'",
            f"update bajiezu.order_info set rent_start_time = DATE_SUB(rent_start_time, INTERVAL 1 YEAR),"
            f"rent_end_time = CURDATE() - INTERVAL {overdue_days} DAY WHERE order_id = '{order_id}'"
        ]
        return self.db_manager.execute_sql_list(sql_list)

    def execute_scenario_d_sql(self, order_id, modify_bill_date=False, term=None, adjust_days=None):
        """执行租用中场景的SQL语句"""
        sql_list = [
            f"update bajiezu.`order` set order_status = '50', sub_status = '50' where order_id = '{order_id}'",
            f"UPDATE `bajiezu`.`order_bill` SET `status` = '10' where order_id = '{order_id}' and now_lease_term < {term}"
        ]

        if modify_bill_date and term is not None and adjust_days is not None:
            sql_list.append(
                f"UPDATE `bajiezu`.`order_bill` SET `bill_due_date` = CURDATE() + INTERVAL {adjust_days} DAY "
                f"WHERE order_id = '{order_id}' and now_lease_term = {term}"
            )
        
        return self.db_manager.execute_sql_list(sql_list)

    def execute_scenario_e_sql(self, order_id):
        """执行恢复待发货场景的SQL语句"""
        if not self._ensure_connection():
            return False
        
        sql_list = [
            f"update bajiezu.`order` set order_status = 40, sub_status = 40 where order_id = '{order_id}'",
            f"update bajiezu.`order_bill` set `status` = '0' where order_id = '{order_id}' and now_lease_term > 1",
            f"delete from bajiezu.`order_bill` where order_id = '{order_id}' and type = 2",
            f"delete from bajiezu.`order_overdue_rent_resale_record` WHERE order_id = '{order_id}'",
            f"DELETE FROM `bajiezu`.`order_return_overdue` WHERE order_id = '{order_id}'",
            f"DELETE FROM `bajiezu`.`order_bill_payable_detail` WHERE order_id = '{order_id}' and type = 4"
        ]
        result = self.db_manager.execute_sql_list(sql_list)
        self.close_connection()  # 确保操作完成后关闭连接
        return result