"""
项目启动相关配置:
1. 数据库配置
2. redis配置
3. session配置, 为后续登陆保持做铺垫
4. 日志文件配置
5. CSRFProtect配置, 为了对,'POST','PUT','DISPATCH','DELETE'做保护
6. 迁移配置


"""""
from flask import Flask
from flask import session
from info import create_app

app = create_app("develop")

@app.route('/',methods=["POST"])
def helloworld():

    # 测试redis存储数据
    # redis_store.set("name","laowang")
    # print(redis_store.get("name"))

    # session["age"] = "13"
    # print(session.get("age"))

    return "helloworld"

if __name__ == "__main__":
    app.run()