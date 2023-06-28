from django.db import models

class Admin(models.Model):
    '''管理员'''
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

class Department(models.Model):
    '''部门表'''
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入学时间")

    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Number(models.Model):
    '''卡号表'''
    number = models.CharField(verbose_name="卡号", max_length=11)
    #想要允许为空，参数： null=True, blank=True
    price = models.IntegerField(verbose_name="价格")

    level_enum = (
        (1, "学生卡"),
        (2, "教师卡"),
        (3, "职工卡"),
        (4, "临时卡"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_enum, default=1)

    status_enum = (
        (1, "未激活"),
        (2, "已激活"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_enum, default=1)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)