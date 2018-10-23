from flask import Blueprint

# 创建蓝图对象
user_blue = Blueprint("user",__name__,url_prefix="/user")

# 装饰试图函数
from . import views