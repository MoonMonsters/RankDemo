# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'

from __future__ import absolute_import
from datetime import timedelta

from celery.schedules import crontab

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
    'rank.utils.tasks',
]
# 需要执行任务的配置
beat_schedule = {
    '定时保存数据': {
        'task': 'rank.utils.tasks.save_rank_values',
        # 设置定时的时间，10秒一次
        # TODO: test
        'schedule': timedelta(seconds=30),
        # 每天凌晨一点执行
        # 'schedule': crontab(minute=0, hour=1),
        'args': ()
    },
}
