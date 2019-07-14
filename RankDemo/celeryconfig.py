from kombu import Queue, Exchange
BROKER_URL = 'redis://127.0.0.1:6379'  # 指定broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定backend

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORTS = (  # 指定需要导入的任务模块
    'rank.utils.celery_task',
)

# 序列化和反序列化方案
CELERY_TASK_SERIALIZER = 'msgpack'
# 读取任务结果一般性能要求不高,所以使用可读性更好的json格式
CELERY_RESULT_SERIALIZER = 'json'
# 任务过期时间
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

# 配置队列（settings.py）
CELERY_QUEUES = (
    Queue('default',
          Exchange('default'),
          routing_key='default'),
)
