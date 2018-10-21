# from info.utils.captcha import captcha
from flask import current_app
from flask import render_template
from flask import session

from info.models import User
from info.modules.index import index_blue





@index_blue.route('/')
def helloworld():
    # 获取用户编号，从session
    user_id = session.get("user_id")

    # 判断用户是否存在
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 将用户的信息转成字典
    dict_data = {
        # 如果user存在,返回左边, 否则返回右边
        "user_info":user.to_dict() if user else ""

    }

    return render_template("news/index.html",data=dict_data)

#处理网站logo,浏览器在运行的时候,自动发送一个GET请求,向/favicon.ico地址
#只需要编写对应的接口,返回一张图片即可
#解决: current_app.send_static_file,自动向static文件夹中寻找指定的资源
@index_blue.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")