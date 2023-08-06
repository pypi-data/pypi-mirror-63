# Easy QuerySet

只是为了方便地使用 Django Models 来写脚本

## 安装

```shell
pip install easy_queryset
```

## 示例

```python
from easy_queryset import models, add_mysql
# 数据库配置
add_mysql('localhost', 'username', 'password', 'example_db')
add_mysql('localhost', 'username', 'password', 'example_db', app_label="example")

class Users(models.Model):
    id = models.CharField()
    name = models.CharField()
    email = models.CharField()

    class Meta:
        app_label = "default" # 指定数据库配置
        db_table = "users"


class Group(models.Model):
    id = models.CharField()
    name = models.CharField()
    email = models.CharField()

    class Meta:
        app_label = "example" # 指定数据库配置
        db_table = "group"

Users.objects.all()
Group.objects.all()
```