import datetime
import sys


def this_month():
    """
    计算这个月的时间
    """
    today = datetime.date.today()

    return datetime.date(year=today.year, month=today.month, day=today.day)


def last_day():
    """
    昨天
    """
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    return datetime.date(year=yesterday.year, month=yesterday.month, day=yesterday.day)


# 今天
RANK_TODAY_DATA_KEY = 'rank_today_data:' + str(datetime.date.today())
# 昨天
RANK_YESTERDAY_DATA_KEY = 'rank_today_data:' + str(last_day())
# 这个月
RANK_MONTH_DATA_KEY = 'rank_month_data:' + str(this_month())
# int类型的最大值
INT_MAX_VALUE = sys.maxsize
