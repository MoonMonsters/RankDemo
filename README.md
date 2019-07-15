### 安装
```python
pip install -r requirements.txt
```

### 创建数据表
```python
python manage.py migrate
```

### 创建虚拟数据
```python
python manage.py random_values
python manage.py random_rank
```

### 运行程序
```python
python manage.py runserver
```

### 执行celery
-B 执行定时任务
-A 执行异步任务
```python
celery -B -A RankDemo worker
```

### admin添加任务
也可以进入后台`http://127.0.0.1:8000/admin/django_celery_beat/periodictask/`，添加定时任务，前提是安装了`django-celery-beat==1.5.0`库

### 任务监控
```python
pip install flower
```
启动并进入
```python
celery flower
```
`127.0.0.1:5555`


### 访问
访问链接有三个:
`http://127.0.0.1:8000/rank/?rtype=month` 访问当月排行榜
`http://127.0.0.1:8000/rank/?rtype=today` 访问今日排行榜
`http://127.0.0.1:8000/search/?key=Ann` 搜索时返回的值的搜索量+1