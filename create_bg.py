from PIL import Image

# 创建一个灰色背景图片
img = Image.new('RGB', (1920, 1080), (200, 200, 200))
img.save('static/images/background.png')