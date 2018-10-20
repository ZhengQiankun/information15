"""
项目启动相关配置:
1. 数据库配置
2. redis配置
3. session配置, 为后续登陆保持做铺垫
4. 日志文件配置
5. 迁移配置


"""""
from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session

app = Flask(__name__)

# 配置信息
class Config(object):
    # 调试模式
    DEBUG = True
    SECRET_KEY = "HDSJHFISHFHI"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@localhost:3306/information15"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 3600*24*2  #两天有效期,单位秒

app.config.from_object(Config)

# 创建SQLAlchemy对象，关联app
db = SQLAlchemy(app)

#创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)

#初始化Session,读取app身上session的配置信息
Session(app)

@app.route('/')
def helloworld():

    # 测试redis存储数据
    redis_store.set("name","laowang")
    print(redis_store.get("name"))

    session["age"] = "13"
    print(session.get("age"))

    return "helloworld"

if __name__ == "__main__":
    app.run()