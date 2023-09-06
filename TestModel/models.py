from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=20)


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateField()
    # 关联出版社一对多，意思就是一个出版社可以有印刷多本书
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    # 多对多，意思就是多个作者可以编写多本书
    authors = models.ManyToManyField("Author")


class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    email = models.EmailField()


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    # 一对一，意思为一个作者对应一个作者详情
    au_detail = models.OneToOneField("AuthorDetail", on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    gender_choices = (
        (0, "女"),
        (1, "男"),
        (2, "保密"),
    )
    gender = models.SmallIntegerField(choices=gender_choices)
    tel = models.CharField(max_length=32)
    addr = models.CharField(max_length=64)
    birthday = models.DateField()


class ApiLogin(models.Model):
    url = models.CharField(max_length=300)
    params = models.CharField(max_length=10000)
    method = models.CharField(max_length=10)

    def __str__(self):
        return self.url


class Users(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class Order(models.Model):
    name = models.CharField(max_length=32)
    price = models.CharField(max_length=32)
    desc = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 套件
class Suite(models.Model):
    name = models.CharField(max_length=100)
    is_fuzz = models.BooleanField(default=False)  # 是否启动fuzz测试
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 套件关联用例表
class SuiteSetCase(models.Model):
    # name = models.CharField(max_length=100)
    suite = models.ForeignKey('Suite', on_delete=models.CASCADE)
    case_id = models.IntegerField(null=True)


# 用例
class Case(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=1000)
    hope = models.CharField(max_length=1000, null=True)

    # # 多个用例关联一个套件
    # suite = models.ForeignKey(Suite, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# 模糊用例配置
class Fuzz(models.Model):
    name = models.CharField(max_length=100, default='')
    # 0表示参数不传内容,-1表示删除此参数,-2表示传超长字符串,-3表示自定义规则,需要配合fuzz_content使用
    fuzz_type = models.IntegerField(default=0)
    fuzz_content = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.name


# 任务表
class Task(models.Model):
    name = models.CharField(max_length=100, default="")
    task_state = models.IntegerField(default=0)  # 0没有在测试，1测试中，2测试完成
    task_type = models.IntegerField(default=0)  # 1实时任务,2定时任务
    start_time = models.CharField(max_length=100, null=True)  # 开始时间
    sum_time = models.CharField(max_length=100, null=True)  # 任务完成总数
    # 关联套件表
    suite = models.ForeignKey("Suite", null=True, on_delete=models.SET_NULL)


# 测试报告
class Report(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=10)
    sum_pass = models.IntegerField(default=0) # 统计测试成功总数
    sum_fail = models.IntegerField(default=0) # 统计测试失败总数
    sum_no_check = models.IntegerField(default=0)
    log = models.CharField(max_length=100, null=True)
    report_path = models.CharField(max_length=100)
    #  套件用例执行的统计情况

    task = models.ForeignKey("Task", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# 测试报告详情
class ReportItem(models.Model):
    report = models.ForeignKey(Report, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    params = models.CharField(max_length=1000)
    hope = models.CharField(max_length=100)
    sum_time = models.CharField(max_length=50)
    fact = models.CharField(max_length=10000)
    result = models.IntegerField(default=0)  # 1通过，-1失败，0不检查

    def __str__(self):
        return self.name
