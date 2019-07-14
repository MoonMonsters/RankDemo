import threading
import datetime

from django_redis import get_redis_connection
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination

from rank.models import Username
from rank.utils.serializers import UsernameSerializer
from rank.utils.paginations import RankPagination
from rank.utils.const import RANK_VALUE_KEY

redis = get_redis_connection()


class RankView(APIView):
    def get(self, request, *args, **kwargs):
        # 按score值获取排序值
        values = redis.zrangebyscore(RANK_VALUE_KEY, 0, 1000000, start=0, num=100, withscores=True)
        # 将byte转str
        values = [(k.decode("utf-8"), int(v)) for k, v in values][::-1]

        return Response(values, status=status.HTTP_200_OK)


class SearchView(generics.ListAPIView):
    """
    搜索
    """
    serializer_class = UsernameSerializer
    pagination_class = RankPagination

    def get_queryset(self):
        key = self.request.query_params.get('key')
        # 模糊搜索
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
                redis.zincrby(RANK_VALUE_KEY, 1, name)
