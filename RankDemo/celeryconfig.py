# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'

"""
配置celery设置
生产环境中不能这么配置，密码之类的需要单独存放
"""
from __future__ import absolute_import
from datetime import timedelta

from kombu import Queue, Exchange
from celery.schedules import crontab

# 使用redis存储任务队列
# broker_url = 'redis://127.0.0.1:6379/7'
# 使用redis存储结果
# result_backend = 'redis://127.0.0.1:6379/8'

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
    '定时保存日榜数据': {
        'task': 'rank.utils.tasks.save_rank_today_data',
        # 设置定时的时间，10秒一次
        # TODO: test
        'schedule': timedelta(seconds=30),
        # 每天凌晨一点执行
        # 'schedule': crontab(minute=0, hour=1),
        'args': ()
    },
    '定时加载月榜数据': {
        'task': 'rank.utils.tasks.load_rank_month_data',
        # 设置定时的时间，10秒一次
        # TODO: test
        'schedule': timedelta(seconds=30),
        # 每天凌晨一点执行
        # 'schedule': crontab(minute=20, hour=1),
        'args': ()
    },
}

celery_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_task', Exchange('for_task'), routing_key='for_task'),
)

celery_routers = {
    '执行for_task任务': {'queue': 'for_task', 'routing_key': 'for_task'}
}

# 配置rabbitmq信息
RABBITMQ_HOSTS = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = '/'
RABBITMQ_USER = 'guest'
RABBITMQ_PWD = 'guest'
broker_url = 'amqp://%s:%s@%s:%d/%s' % (RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_HOSTS, RABBITMQ_PORT, RABBITMQ_VHOST)
