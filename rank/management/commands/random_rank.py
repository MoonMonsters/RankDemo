import random
import datetime

from django.core.management.base import BaseCommand
from django_redis import get_redis_connection

from rank.models import Username, RankData
from rank.utils.const import RANK_TODAY_DATA_KEY

redis = get_redis_connection()


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        随机产生搜索量
        """
        self.__random_today_data(RANK_TODAY_DATA_KEY)
        self.__random_20d_data()

    def __random_today_data(self, key):
        """
        保存某天的所有数据
        """
        for username in Username.objects.all():
            num = random.randint(0, 100000)
            print('>>>name:{name}, num:{num}'.format(name=username.name, num=num))
            redis.zincrby(key, num, username.name)

            self.__save_data_to_db(key, username.name, num)

    def __random_20d_data(self):
        """
        生成20天的排行榜数据
        """
        now = datetime.datetime.now()
        # TODO 按需要调整时间
        for day in range(0, 20):
            pre_day = now - datetime.timedelta(days=day)
            date = datetime.date(year=pre_day.year, month=pre_day.month, day=pre_day.day)
            key = 'rank_today_data:' + str(date)
            self.__random_today_data(key)

    @staticmethod
    def __save_data_to_db(key, name, count):
        """
        将数据保存到数据库
        """
        today = key.split(':')[-1].split('-')
        cache_date = datetime.date(year=int(today[0]), month=int(today[1]), day=int(today[2]))
        data, _ = RankData.objects.get_or_create(value=name, cache_date=cache_date)
        data.count = count
        data.save(update_fields=['count'])
