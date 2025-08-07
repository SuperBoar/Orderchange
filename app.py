from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.order_service import OrderService
from common.log import MyLog as Log

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 在生产环境中应该使用环境变量

# 初始化订单服务
order_service = OrderService()

# 获取日志记录器
logger = Log.get_log().get_logger()

# 应用启动时确保数据库连接
with app.app_context():
    if not order_service.order_repository._ensure_connection():
        logger.warning("数据库连接失败，请检查数据库配置！")


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """登录系统"""
    try:
        # 尝试登录各个系统
        if order_service.login_systems():
            logger.info("系统登录成功")
            return jsonify({'success': True, 'message': '系统登录成功'})
        else:
            logger.warning("系统登录失败，请检查网络连接或联系管理员！")
            return jsonify({'success': False, 'message': '系统登录失败，请检查网络连接或联系管理员！'})
    except Exception as e:
        logger.error(f"登录出错：{str(e)}")
        return jsonify({'success': False, 'message': f'登录出错：{str(e)}'})


@app.route('/execute_scenario', methods=['POST'])
def execute_scenario():
    """执行场景"""
    try:
        # 获取表单数据
        order_id = request.form.get('order_id')
        scenario = request.form.get('scenario')
        
        if not order_id or not scenario:
            logger.warning("订单ID和场景类型不能为空")
            return jsonify({'success': False, 'message': '订单ID和场景类型不能为空'})
        
        # 根据场景类型执行相应操作
        result = False
        message = ''
        
        if scenario == 'a':
            term = int(request.form.get('term', 0))
            overdue_days = int(request.form.get('overdue_days', 0))
            result = order_service.execute_scenario_a(order_id, term, overdue_days)
            message = '账单逾期场景执行完成'
            
        elif scenario == 'b':
            return_days = int(request.form.get('return_days', 0))
            result = order_service.execute_scenario_b(order_id, return_days)
            message = '归还场景执行完成'
            
        elif scenario == 'c':
            sub_scenario = request.form.get('sub_scenario')
            if sub_scenario == 'x':
                term = int(request.form.get('term', 0))
                overdue_days = int(request.form.get('overdue_days', 0))
                result = order_service.execute_scenario_c_x(order_id, term, overdue_days)
                message = '账单逾期租转售场景执行完成'
            elif sub_scenario == 'y':
                overdue_days = int(request.form.get('overdue_days', 0))
                result = order_service.execute_scenario_c_y(order_id, overdue_days)
                message = '归还逾期租转售场景执行完成'
                
        elif scenario == 'd':
            # 处理modify_bill_date参数，可以是'true'/'false'或'on'/'None'
            modify_bill_date_str = request.form.get('modify_bill_date', 'false')
            modify_bill_date = modify_bill_date_str.lower() in ['true', 'on', '1']
            
            term = request.form.get('term')
            adjust_days = request.form.get('adjust_days')
            
            # 处理可能为空的值
            term = int(term) if term else None
            adjust_days = int(adjust_days) if adjust_days else None
            
            result = order_service.execute_scenario_d(
                order_id, 
                modify_bill_date=modify_bill_date, 
                term=term, 
                adjust_days=adjust_days
            )
            message = '租用中场景执行完成'
            
        elif scenario == 'e':
            result = order_service.execute_scenario_e(order_id)
            message = '恢复待发货状态场景执行完成'
            
        elif scenario == 'f':
            order_service.execute_scenario_f()
            result = True
            message = '生成代扣参数场景执行完成'
            
        if result:
            logger.info(f"订单 {order_id} 场景 {scenario} 执行成功")
            return jsonify({'success': True, 'message': f'{message} - 数据修改成功！'})
        else:
            logger.warning(f"订单 {order_id} 场景 {scenario} 执行失败")
            return jsonify({'success': False, 'message': f'{message} - 数据修改失败！'})
            
    except Exception as e:
        logger.error(f"执行订单 {order_id} 场景 {scenario} 出错：{str(e)}")
        return jsonify({'success': False, 'message': f'执行出错：{str(e)}'})


@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy'})


# 在应用关闭时关闭数据库连接
@app.teardown_appcontext
def close_db_connection(error):
    if error:
        logger.error(f"应用关闭时出现错误: {error}")
    # 注意：这里我们不主动关闭连接，让连接保持以便复用
    # 如果需要强制关闭，可以取消下面一行的注释
    # order_service.order_repository.close_connection()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)