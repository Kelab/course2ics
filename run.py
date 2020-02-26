from os import getenv as _, environ
from dotenv import load_dotenv

# 必须先与后面的 gen 之前加载, 配置好 env
load_dotenv()
environ["no_proxy"] = "*"

from auth_swust import Login
from loguru import logger

from gen_ics import generate_class_schedule
from parse_api import get_course_api


# 登录部分
username = _("c2i_username")
password = _("c2i_password")
path = _("c2i_path", "./")

if not username or not password:
    logger.error("未设置用户名密码")
    raise ValueError("未设置用户名密码")

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
        logger.error(f"{u} 生成日历出错！")
