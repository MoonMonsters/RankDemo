# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'

from __future__ import absolute_import
from celery.schedules import crontab
from datetime import timedelta

# 使用redis存储任务队列
broker_url = 'redis://127.0.0.1:6379/7'
# 使用redis存储结果
result_backend = 'redis://127.0.0.1:6379/8'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
# 时区设置
timezone = 'Asia/Shanghai'
# celery默认开启自己的日志
# False表示不关闭
worker_hijack_root_logger = False
# 存储结果过期时间，过期后自动删除
# 单位为秒
result_expires = 60 * 60 * 24

# 导入任务所在文件
imports = [
    'rank.tasks',
]
10
# 需要执行任务的配置
beat_schedule = {
    # 'test1': {
    #     # 具体需要执行的函数
    #     # 该函数必须要使用@app.task装饰
    #     'task': 'celery_task.app_scripts.test1.test1_run',
    #     # 定时时间
    #     # 每分钟执行一次，不能为小数
    #     'schedule': crontab(minute='*/1'),
    #     # 或者这么写，每小时执行一次
    #     # "schedule": crontab(minute=0, hour="*/1")
    #     # 执行的函数需要的参数
    #     'args': ()
    # },
    '定时保存数据': {
        'task': 'rank.tasks.save_rank_values',
        # 设置定时的时间，10秒一次
        'schedule': timedelta(seconds=30),
        'args': ()
    },
    '定时打印数据': {
        'task': 'rank.tasks.interval_print',
        # 设置定时的时间，10秒一次
        'schedule': timedelta(seconds=10),
        'args': ()
    }
}
