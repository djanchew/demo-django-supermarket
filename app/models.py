from django.db import models


# 管理员表
class Manager(models.Model):
    account = models.CharField(max_length=20)   # 登陆账号
    pwd = models.CharField(max_length=40)       # 登陆密码

    name = models.CharField(max_length=20)      # 管理员名字，记录操作
    gender = models.IntegerField(default=0)     # 0女 1男
    phone = models.CharField(max_length=11)     # 电话，联系
    authority = models.IntegerField(default=0)  # 权限，[0]超级管理员，[1]经理，[2]采购员，[3]售货员

    isDelete = models.BooleanField(default=0)   # 逻辑删除 0存在 1删除


# 供应商表
class Provider(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    phone = models.CharField(max_length=11)

    isDelete = models.BooleanField(default=False)


# 商品表
class Goods(models.Model):
    name = models.CharField(max_length=20)       # 图片命名为0_name.png??
    # img = models.ImageField(upload_to='goods_img/')
    sale_price = models.FloatField()             # 出售价格
    cost_price = models.FloatField()             # 进货价格
    weight = models.FloatField()                 # 重量
    sort = models.IntegerField()                 # 类别：[0]零食饮料 [1]生鲜果蔬 [2]粮油副食 [3]清洁用品 [4]家居家电
    # location = models.IntegerField()             # 所在超市 4东、2三、1一，[0] [3]一饭三饭 [5]一饭东区 [6]三饭东区 [7]全有

    produce_date = models.DateField()            # 生产日期
    limit_date = models.DateField()              # 使用期限
    # preserve = models.IntegerField()             # 保质期

    # isHot = models.IntegerField(null=True)       # 如果不为0或null，则往上增加，作为热度指标
    # isCheap = models.IntegerField(null=True)     # 热度长时间为0或null，或者临期，则考虑降价出售
    lower = models.FloatField(default=0)         # 改成浮点，后台输入数字，然后定义减法降价

    provider = models.ForeignKey(Provider, on_delete=True)

    isDelete = models.BooleanField(default=False)


# 记录表  # 都可为null，用一张表存储进货和出货两种记录
class Record(models.Model):
    location = models.IntegerField()                 # 发生的超市位置
    date = models.DateField(auto_now=True)           # 发生的日期
    purchase_num = models.IntegerField(null=True)    # 进货数量  # 库存=所有进货记录-所有出售记录
    sale_num = models.IntegerField(null=True)        # 出售数量  # 销量=所有出售记录
    withdraw_num = models.IntegerField(null=True)                 # 下架退回  # 好像没有用到的地方

    goods = models.ForeignKey(Goods, on_delete=True)


# 消息表  # 反馈/系统消息/职员消息
class Message(models.Model):
    time = models.DateTimeField(auto_now=True)   # 消息发送时间  # auto_now只有一次，auto_now_add可以继续添加新的值，即改变值
    type = models.IntegerField()    # [0]系统消息，由管理员发送，或者自动发送，全员接收 [1]反馈消息
    content = models.TextField()
    contact = models.CharField(max_length=20)    # 联系方式，同下
    name = models.CharField(max_length=20)       # 姓名，在js控制，如果输入为空则存为匿名用户

    isRead = models.BooleanField(default=False)


# 登陆，进货-->
# 基本功能要求：
# 1.	商品的进、出货操作；
# 2.	进、出货记录和库存记录的查询；
# 3.	商品信息管理；
# 4.	系统设置。
# 5.	系统登陆与注销
# 根据职位不同，分别具有如下功能：
# 1)	销售员：商品查价、出售、退货、账单记录等；-------------商品表：增删改
# 2)	经理：账本管理、调整商品价格、上下架、库存记录查询等；
# 3)	采购员：对库存进行增删改，进出货记录等；
# 4)	系统管理员：分配系统账号和权限等。
