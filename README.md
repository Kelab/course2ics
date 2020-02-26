# course2ics

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 依赖项

依赖 `auth_swust >= 1.2.7`，该包的使用请见： <https://github.com/BuddingLab/auth_swust>
主要是需要**手动安装** `keras, tensorflow` 或 `pytorch`。

```bash
pip install auth-swust
```

## 如何启动

你需要一个 Python 环境， 然后执行：

```bash
pip install -r requirements.txt
```

## 课表生成使用方法

在本目录下新建一个`.env`文件，代码如下：
path 选项可不填，默认当前目录

```env
username=51xxxx
password=xxxxxx
path=../
```

要同时生成多个日历，可以使用`,`将不同用户名密码分隔开，用户名密码一一对应：

```env
username=51xxxx1,51xxxx2,51xxxx3
password=xxxxxx1,xxxxxx2,xxxxxx3
```

然后运行`run.py`文件，即可在当前目录下生成日历文件。

```python
python run.py
```

> 如果上传到谷歌日历发现没有按时提醒，请在谷歌日历网页版设置中打开活动通知功能。
