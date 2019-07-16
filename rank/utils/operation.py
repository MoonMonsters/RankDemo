# !/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'ChenTao'

from django.db.models.aggregates import Sum
from django_redis import get_redis_connection

from rank.models import RankData
from rank.utils.const import RANK_MONTH_DATA_KEY, this_month

redis = get_redis_connection()


def load_rank_month_data_db2redis():
    """
    从db中加载月排行榜数据到redis中
    """
    _this_month = this_month()
    # 使用聚合函数，分类计算每个产品的搜索量
    data = RankData.objects \
        .filter(cache_date__year=_this_month.year, cache_date__month=_this_month.month) \
        .values('value') \
        .distinct() \
        .annotate(count=Sum('count')) \
        .order_by('-count')
    values = list(data[:100])
    # 将从数据库中读取的数据，放到redis中
    if values:
        for value in values:
            v = value.get('value')
            count = value.get('count')
            redis.zincrby(RANK_MONTH_DATA_KEY, count, v)

    return values
