from __future__ import absolute_import

import datetime

from django_redis import get_redis_connection

from RankDemo.celery import app
from rank.models import RankData
from rank.utils.const import RANK_YESTERDAY_DATA_KEY, INT_MAX_VALUE

redis = get_redis_connection()


@app.task()
def save_rank_values():
    """
    将每天的排行榜数据存入到数据库中，同时删除redis中的数据
    """
    print('>>> 保存缓存中的排名数据到数据库中...')
    values = redis.zrangebyscore(RANK_YESTERDAY_DATA_KEY, 0, INT_MAX_VALUE, start=0, num=100, withscores=True)
    # 保存缓存数据都是放在十二点以后，所以要获取前一天的缓存数据
    today = RANK_YESTERDAY_DATA_KEY.split(':')[-1].split('-')
    cache_date = datetime.date(year=int(today[0]), month=int(today[1]), day=int(today[2]))
    # 保存缓存到数据库
    for name, count in values:
        data, _ = RankData.objects.get_or_create(value=name.decode('utf-8'), cache_date=cache_date)
        data.count = count
        data.save(update_fields=['count'])

    # TODO 为什么无法调用delete函数？明明存在
    _del = getattr(redis, 'delete')
    print('>>>_del.type = ' + str(_del))
    # 删除缓存
    # if hasattr(redis, 'delete'):
    #     _del = getattr(redis, 'delete')
    #     print('>>>_del = ' + str(_del))
    #     redis.delele(RANK_YESTERDAY_DATA_KEY)
    # else:
    redis.zremrangebyscore(RANK_YESTERDAY_DATA_KEY, 0, INT_MAX_VALUE)
