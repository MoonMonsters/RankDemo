from __future__ import absolute_import

import datetime

from django_redis import get_redis_connection

from RankDemo.celery import app
from rank.models import RankData
from rank.utils.const import RANK_YESTERDAY_DATA_KEY, INT_MAX_VALUE, RANK_TODAY_DATA_KEY
from rank.utils.operation import load_rank_month_data_db2redis

redis = get_redis_connection()


@app.task()
def save_rank_today_data():
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
    # _del = getattr(redis, 'delete')
    # print('>>>_del.type = ' + str(_del))
    # 删除缓存
    # if hasattr(redis, 'delete'):
    #     _del = getattr(redis, 'delete')
    #     print('>>>_del = ' + str(_del))
    #     redis.delele(RANK_YESTERDAY_DATA_KEY)
    # else:
    # TODO: 使用时需要打开此行代码
    # 按搜索量区间删除数据（delete函数无法使用）
    redis.zremrangebyscore(RANK_YESTERDAY_DATA_KEY, 0, INT_MAX_VALUE)


@app.task()
def load_rank_month_data():
    """
    每天计算一次当月排行榜，加载进redis中
    """
    print('>>> 从数据库中读取月排行榜数据到缓存中...')
    load_rank_month_data_db2redis()


@app.task()
def add_rank_value(models):
    """
    每次搜索时，搜索值都加1
    """
    print('>>> 执行异步任务，搜索量+1')
    for model in list(models):
        for _, name in model.items():
            redis.zincrby(RANK_TODAY_DATA_KEY, 1, name)
