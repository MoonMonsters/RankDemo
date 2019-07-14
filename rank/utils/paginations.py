from rest_framework import pagination


class RankPagination(pagination.PageNumberPagination):
    # 默认值 ，每一页的数量，如果没有size参数的话
    page_size = 8
    # 最大数量，即使 带上了size参数，也无法超过这个值
    max_page_size = 10
    # 通过GET请求获取每一页需要的数量，/?size=x的size参数
    page_size_query_param = 'size'
    # url中要查找的page参数，即/?page=x中的page参数
    page_query_param = 'page'
