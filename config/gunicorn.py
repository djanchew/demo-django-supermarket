# bind = '0.0.0.0:8123'

# workers = 1
# worker_class = 'gevent'
# reload = False
# preload_app = False
#
# accesslog = '-'
# errorlog = '-'
#
# log_level = 'info'
# # 生产环境一般不在这里写gunicorn的配置文件, 而在supervisor的配置文件中覆盖

import multiprocessing

bind = '0.0.0.0:8123'
workers = 2  # 核心数
errorlog = '/home/ubuntu/workspace/Django-demo__/logs/gunicorn.error.log'  # 发生错误时log的路径
accesslog = '/home/ubuntu/workspace/Django-demo__/logs/gunicorn.access.log'  # 正常时的log路径
# loglevel = 'debug'   #日志等级
proc_name = 'gunicorn_project'  # 进程名
