from modules.index import index_blue


@index_blue.route('/')
def helloworld():

    # 测试redis存储数据
    # redis_store.set("name","laowang")
    # print(redis_store.get("name"))

    # session["age"] = "13"
    # print(session.get("age"))

    #输入记录信息, 可以替代print
    # logging.debug("调试信息1")
    # logging.info("详细信息1")
    # logging.warning("警告信息1")
    # logging.error("错误信息1")

    #上面的方式可以写成,current_app来输出,区别在于控制台有华丽分割线隔开,写入到文件是一样的
    # current_app.logger.debug("调试信息2")
    # current_app.logger.info("详细信息2")
    # current_app.logger.warning("警告信息2")
    # current_app.logger.error("错误信息2")
    return "helloworld"