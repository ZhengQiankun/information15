from flask import abort, jsonify
from flask import current_app
from flask import g
from flask import session

from info.models import News, User
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import news_blue
from flask import render_template

#功能描述: 获取新闻详细信息
# 请求路径: /news/<int:news_id>
# 请求方式: GET
# 请求参数:news_id
# 返回值: detail.html页面, 用户data字典数据
@news_blue.route('/<int:news_id>')
@user_login_data
def news(news_id):
    """
    # 思路分析
    # 1.根据传入的新闻编号,获取新闻对象
    # 2.判断新闻是否存在
    # 3.查询热门新闻数据
    # 4.将新闻列表转成,字典列表
    # 5.携带数据渲染页面
    """
    # 1 根据传入的新闻编号,获取新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg = "新闻获取失败")


    # 2 判断新闻是否存在
    if not news:
        abort (404)

    # 3 查询热门新闻数据
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(8).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询数据失败")


    # 4 将新闻列表转成,字典列表
    click_news_list = []
    for item in news_list:
        click_news_list.append(item.to_dict())

    # 查询当前用户，是否收藏该新闻
    is_collected = False
    if g.user and news in g.user.collection_news:
        is_collected = True


    data = {
        "news":news.to_dict(),
        "click_news_list":click_news_list,
        "user_info":g.user.to_dict() if g.user else "",
        "is_collected":is_collected
    }

    # 5 携带数据渲染页面
    return render_template("news/detail.html",data = data)


