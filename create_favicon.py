from PIL import Image
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, 'static', 'images', 'bajiezu.png')
favicon_path = os.path.join(current_dir, 'static', 'favicon.ico')

# 打开背景图片并创建 favicon
try:
    # 打开背景图片
    img = Image.open(background_path)
    
    # 调整大小为 favicon 标准尺寸
    img = img.resize((32, 32), Image.LANCZOS)
    
    # 保存为 favicon.ico
    img.save(favicon_path, format='ICO')
    
    print(f"favicon.ico 已成功创建在 {favicon_path}")
except Exception as e:
    print(f"创建 favicon.ico 时出错: {e}")