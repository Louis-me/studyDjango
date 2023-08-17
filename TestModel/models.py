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


class Users(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

class Order(models.Model):
    name = models.CharField(max_length=32)
    price = models.CharField(max_length=32)
    desc = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
