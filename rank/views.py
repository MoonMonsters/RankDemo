import threading

from django_redis import get_redis_connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rank.models import Username
from rank.utils.serializers import UsernameSerializer
from rank.utils.paginations import RankPagination
from rank.utils.const import RANK_TODAY_DATA_KEY, RANK_MONTH_DATA_KEY, INT_MAX_VALUE
from rank.utils.operation import load_rank_month_data_db2redis
from rank.utils.tasks import add_rank_value

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
            values = self.__get_today_rank_data()
        # 当月排行榜
        elif rank_type == RANK_TYPE_MONTH:
            values = self.__get_last_month_rank_data()

        return Response(values, status=status.HTTP_200_OK)

    @staticmethod
    def __get_today_rank_data():
        """
        获取今天排行榜
        """
        # 按score值获取排序值
        values = redis.zrangebyscore(RANK_TODAY_DATA_KEY, 0, INT_MAX_VALUE, start=0, num=100, withscores=True)
        # 将byte转str
        values = [{'value': k.decode("utf-8"), 'count': int(v)} for k, v in values][::-1]

        return values

    @staticmethod
    def __get_last_month_rank_data():
        """
        获取本月排行榜
        """
        # 按score值获取排序值
        values = redis.zrangebyscore(RANK_MONTH_DATA_KEY, 0, INT_MAX_VALUE, start=0, num=100, withscores=True)
        if values:
            # 将byte转str
            values = [{'value': k.decode("utf-8"), 'count': int(v)} for k, v in values][::-1]
        else:
            # 如果缓存中没有月榜数据，就从数据库中读取
            values = load_rank_month_data_db2redis()

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

        # 执行异步任务， 搜索量+1
        add_rank_value.apply_async(args=(serializer.data,), routing_key='for_task', queue='for_task')

        return Response(serializer.data, status=status.HTTP_200_OK)
