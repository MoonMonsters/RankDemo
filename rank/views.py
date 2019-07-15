import threading
import sys

from django_redis import get_redis_connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rank.models import Username, RankData
from rank.utils.serializers import UsernameSerializer
from rank.utils.paginations import RankPagination
from rank.utils.const import RANK_TODAY_DATA_KEY, RANK_MONTH_DATA_KEY, this_month

redis = get_redis_connection()

RANK_TYPE_TODAY = 'today'
RANK_TYPE_MONTH = 'month'


class RankView(APIView):
    """
    排行榜数据
    """

    def get(self, request, *args, **kwargs):

        rank_type = self.request.query_params.get('rtype')
        values = None

        # 今日排行榜
        if rank_type == RANK_TYPE_TODAY:
            values = self._get_today_rank_data()
        # 上月排行榜
        elif rank_type == RANK_TYPE_MONTH:
            values = self._get_last_month_rank_data()

        return Response(values, status=status.HTTP_200_OK)

    @staticmethod
    def _get_today_rank_data():
        """
        获取今天排行榜
        """
        # 按score值获取排序值
        values = redis.zrangebyscore(RANK_TODAY_DATA_KEY, 0, sys.maxsize, start=0, num=100, withscores=True)
        # 将byte转str
        values = [{'value': k.decode("utf-8"), 'count': int(v)} for k, v in values][::-1]

        return values

    @staticmethod
    def _get_last_month_rank_data():
        """
        获取本月排行榜
        """
        # 按score值获取排序值
        values = redis.zrangebyscore(RANK_MONTH_DATA_KEY, 0, sys.maxsize, start=0, num=100, withscores=True)
        if values:
            # 将byte转str
            values = [{'value': k.decode("utf-8"), 'count': int(v)} for k, v in values][::-1]
        else:
            _this_month = this_month()
            from django.db.models.aggregates import Sum
            data = RankData.objects.filter(cache_date__year=_this_month.year,
                                           cache_date__month=_this_month.month).values(
                'value').distinct().annotate(count=Sum('count')).order_by('-count')
            values = list(data[:100])
            # 将从数据库中读取的数据，放到redis中
            if values:
                for value in values:
                    v = value.get('value')
                    count = value.get('count')
                    redis.zincrby(RANK_MONTH_DATA_KEY, count, v)

        return values


class SearchView(generics.ListAPIView):
    """
    搜索
    """
    serializer_class = UsernameSerializer
    pagination_class = RankPagination

    def get_queryset(self):
        key = self.request.query_params.get('key')
        # 模糊搜索
        # 模糊搜索出来的数据，都要计算+1
        return Username.objects.filter(name__icontains=key)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)

        # 子线程中去计算+1
        threading.Thread(target=self._add_rank_value, args=(serializer.data,)).start()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def _add_rank_value(models):
        """
        每次搜索时，搜索值都加1
        """
        for model in list(models):
            for _, name in model.items():
                redis.zincrby(RANK_TODAY_DATA_KEY, 1, name)
