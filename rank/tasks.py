from __future__ import absolute_import

import time
import datetime

from celery.utils.log import get_task_logger
from django_redis import get_redis_connection

from RankDemo.celery import app
from rank.models import RankData
from rank.utils.const import RANK_VALUE_KEY

redis = get_redis_connection()


@app.task
def save_rank_values():
    print('>>> 保存缓存中的排名数据到数据库中...')
    values = redis.zrangebyscore(RANK_VALUE_KEY, 0, 1000000, start=0, num=100, withscores=True)
    today = RANK_VALUE_KEY.split(' ')[-1].split('-')
    cache_date = datetime.date(year=today[0], month=today[1], day=today[2])
    for name, count in values:
        data, _ = RankData.objects.get_or_create(name=name, cache_date=cache_date)
        data.count = count
        data.save(update_fields=['count'])

    return str(time.time())


@app.task
def interval_print():
    get_task_logger('hello').debug('hhhhhhhhhhhhh')
    print('>>>>>>>>ppppprint')

    with open('test.log', 'w+') as fp:
        fp.write(str(time.time()))
