# from info.utils.captcha import captcha
from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from info.models import User, News, Category
from info.modules.index import index_blue
from info.utils.common import user_login_data
from info.utils.response_code import RET

#功能描述: 获取首页新闻内容
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据

@index_blue.route('/newslist')
@user_login_data
def newslist():
    """
    1. 获取参数
    2. 参数类型转换
    3. 分页查询
    4. 获取分页对象属性,总页数,当前页,当前页对象
    5. 将当前页对象列表,转成字典列表
    6. 响应,返回json数据
    :return:
    """

    # 1. 获取参数
    cid = request.args.get("cid","1")
    page = request.args.get("page","1")
    per_page = request.args.get("per_page","10")

    # 2. 参数类型转换
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1,
        per_page = 10


    # 3. 分页查询
    try:
        # 判断分类编号是否,不等1,最新分类是按照时间倒序排列的
        filters = []
        if cid != "1":
            filters.append(News.category_id == cid)
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="分页查询失败")



    # 4. 获取分页对象属性,总页数,当前页,当前页对象
    totalPages = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5. 将当前页对象列表,转成字典列表
    newsList = []
    for item in items:
        newsList.append(item.to_dict())

    # 6. 响应,返回json数据
    return jsonify(errno=RET.OK,errmsg = "获取成功",totalPages = totalPages,currentPage = currentPage,newsList = newsList)


@index_blue.route('/')
@user_login_data
def show_index():

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

    # 查询所有的分类信息
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="分类查询失败")

    # 将分类的对象列表,转成字典列表
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())



    # 将用户的信息转成字典
    dict_data = {
        # 如果user存在,返回左边, 否则返回右边
        "user_info":g.user.to_dict() if g.user else "",
        "click_news_list":click_news_list,
        "categories":category_list

    }

    return render_template("news/index.html",data=dict_data)

#处理网站logo,浏览器在运行的时候,自动发送一个GET请求,向/favicon.ico地址
#只需要编写对应的接口,返回一张图片即可
#解决: current_app.send_static_file,自动向static文件夹中寻找指定的资源
@index_blue.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file("news/favicon.ico")