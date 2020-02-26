import os
import sys

os.environ["no_proxy"] = "*"
os.environ["CAPTCHA_BACKEND"] = "keras"

from auth_swust import Login, default_logger
from parse_api import get_course_api
from gen_ics import generate_class_schedule

from loguru import logger

logger.remove(default_logger)
logger.add(sys.stdout, level="DEBUG")

if not os.path.exists(".env"):
    print("未找到 .env 配置文件")

with open(".env") as f:
    local_env = dict()
    content = f.readlines()
    for line in content:
        line = line.strip()
        _k, _v = line.split("=")
        local_env[_k.strip()] = _v.strip()

# 登录部分
username = local_env.get("username")
password = local_env.get("password")
path = local_env.get("path", "")

if not username or not password:
    print("未设置用户名密码")
    exit("0")

username_li = username.split(",")
password_li = password.split(",")

for u, p in zip(username_li, password_li):
    login = Login(u, p)
    res, _ = login.try_login()
    if res:
        sess = login.sess
        api = get_course_api(sess)
        generate_class_schedule(api, u, path)
    else:
        print(f"{u} 生成日历出错！")
