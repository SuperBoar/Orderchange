from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.order_service import OrderService

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 在生产环境中应该使用环境变量

# 初始化订单服务
order_service = OrderService()


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
            return jsonify({'success': True, 'message': '系统登录成功'})
        else:
            return jsonify({'success': False, 'message': '系统登录失败，请检查网络连接或联系管理员！'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'登录出错：{str(e)}'})


@app.route('/execute_scenario', methods=['POST'])
def execute_scenario():
    """执行场景"""
    try:
        # 获取表单数据
        order_id = request.form.get('order_id')
        scenario = request.form.get('scenario')
        
        if not order_id or not scenario:
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
            
        if result:
            return jsonify({'success': True, 'message': f'{message} - 数据修改成功！'})
        else:
            return jsonify({'success': False, 'message': f'{message} - 数据修改失败！'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'执行出错：{str(e)}'})


@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)