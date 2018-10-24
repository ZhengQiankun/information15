from flask import current_app
from flask import g, jsonify
from flask import redirect
from flask import request

from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import user_blue
from flask import render_template

# 功能描述: 密码修改
# 请求路径: /user/pass_info
# 请求方式:GET,POST
# 请求参数:GET无, POST有参数,old_password, new_password
# 返回值:GET请求: user_pass_info.html页面,data字典数据, POST请求: errno, errmsg
@user_blue.route('/pass_info', methods=['GET', 'POST'])
@user_login_data
def pass_info():
    # 1.如果请求方式为GET，直接返回页面渲染
    if request.method == "GET":
        return render_template("news/user_pass_info.html")

    # 2.获取参数
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")


    # 3.校验参数
    if not all([old_password,new_password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")

    # 4.判断原密码是否正确
    if g.user.check_password(old_password):
        return jsonify(errno=RET.PARAMERR,errmsg="原密码输入错误")

    # 5.修改密码信息
    g.user.password = new_password

    # 6.返回响应
    return jsonify(errno=RET.OK,errmsg="修改密码成功")


# 功能描述: 获取基本资料
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@user_blue.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():
    # 1判读是否为post请求
    if request.method == "GET":
        return render_template("news/user_base_info.html",user=g.user.to_dict())
    # 2获取参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2.1校验参数，为空校验
    if not all([nick_name,signature,gender]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    # 2.2性别校验

    if gender not in ["WOMAN","MAN"]:
        return jsonify(errno=RET.DATEERR, errmsg="性别异常")

    # 3,修改用户信息
    try:
        g.user.nick_name = nick_name
        g.user.signature = signature
        g.user.gender = gender

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBEERR, errmsg="修改失败")


    # 4.返回响应
    return jsonify(errno=RET.OK, errmsg="修改成功")


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