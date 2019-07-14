import random

from django.core.management.base import BaseCommand
from django_redis import get_redis_connection

from rank.models import Username
from rank.utils.const import RANK_VALUE_KEY

redis = get_redis_connection()


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        随机产生搜索量
        """
        for username in Username.objects.all():
            num = random.randint(0, 100000)
            redis.zincrby(RANK_VALUE_KEY, num, username.name)
