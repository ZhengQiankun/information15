from . import user_blue
from flask import render_template

#展示个人中心页面
# 请求路径: /user/info
# 请求方式:GET
# 请求参数:无
# 返回值: user.html页面,用户字典data数据
@user_blue.route('/info')
def user_index():
    return render_template("news/user.html")