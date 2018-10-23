from flask import g
from flask import redirect

from info.utils.common import user_login_data
from . import user_blue
from flask import render_template

# 功能描述: 获取基本资料
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@user_blue.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():

    return render_template("news/user_base_info.html",user=g.user.to_dict())

#展示个人中心页面
# 请求路径: /user/info
# 请求方式:GET
# 请求参数:无
# 返回值: user.html页面,用户字典data数据
@user_blue.route('/info')
@user_login_data
def user_index():

    if not g.user:
        return redirect("/")
    data = {
        "user_info":g.user.to_dict() if g.user else ""
    }
    return render_template("news/user.html",data = data)