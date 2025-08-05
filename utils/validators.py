def validate_int_input(prompt):
    """
    验证整数输入
    
    Args:
        prompt (str): 提示信息
        
    Returns:
        int: 用户输入的正整数
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("输入错误，请输入非负整数！")
        except ValueError:
            print("输入错误，请输入整数！")


def validate_yes_no(prompt):
    """
    验证y/n输入
    
    Args:
        prompt (str): 提示信息
        
    Returns:
        str: 'y' 或 'n'
    """
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'n']:
            return choice
        print("输入错误，请输入 y 或 n！")


def validate_choice(prompt, valid_choices):
    """
    验证选项输入
    
    Args:
        prompt (str): 提示信息
        valid_choices (list): 有效选项列表
        
    Returns:
        str: 有效的选项
    """
    while True:
        choice = input(prompt).lower()
        if choice in valid_choices:
            return choice
        print(f"输入错误，请输入有效的选项: {', '.join(valid_choices)}！")


__all__ = ['validate_int_input', 'validate_yes_no', 'validate_choice']