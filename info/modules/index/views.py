# from info.utils.captcha import captcha
from flask import current_app, jsonify
from flask import render_template
from flask import session

from info.models import User, News
from info.modules.index import index_blue
from info.utils.response_code import RET


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

    # 查询数据库,根据点击量查询前十条新闻
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10) .all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="新闻查询异常")

    # 将新闻对象列表, 转成字典列表
    click_news_list = []
    for news in news_list:
        click_news_list.append(news.to_dict())


    # 将用户的信息转成字典
    dict_data = {
        # 如果user存在,返回左边, 否则返回右边
        "user_info":user.to_dict() if user else "",
        "click_news_list":click_news_list

    }

    return render_template("news/index.html",data=dict_data)

#处理网站logo,浏览器在运行的时候,自动发送一个GET请求,向/favicon.ico地址
#只需要编写对应的接口,返回一张图片即可
#解决: current_app.send_static_file,自动向static文件夹中寻找指定的资源
@index_blue.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")