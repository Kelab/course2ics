import os
from auth_swust import Login
from auth_swust.log import AuthLogger, DEBUG
from parse_api import get_course_api
from gen_ics import generate_class_schedule

AuthLogger.setLevel(DEBUG)

if not os.path.exists('.env'):
    print('未找到 .env 配置文件')

with open('.env') as f:
    local_env = dict()
    content = f.readlines()
    for line in content:
        line = line.strip()
        _k, _v = line.split('=')
        local_env[_k.strip()] = _v.strip()

# 登录部分
username = local_env.get('username')
password = local_env.get('password')
path = local_env.get('path', '')

if username and password:
    login = Login(username, password)
    res, _ = login.try_login()
    if res:
        sess = login.sess
        api = get_course_api(sess)
        print(api)
        generate_class_schedule(api, username, path)
    else:
        print("Error")
