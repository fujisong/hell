# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
#import sys
from django.db import models
#reload(sys)
#sys.setdefaultencoding('utf8')

# Create your models here.
#发布会表
class Event(models.Model):
    name=models.CharField(max_length=100)
    limit=models.IntegerField()               #参加人数
    status=models.BooleanField()
    address=models.CharField(max_length=200)
    start_time=models.DateTimeField('events time')
    create_time=models.DateTimeField(auto_now=True)   #创建时间（自动获取当前时间）

    def __str__(self):
        return self.name

#嘉宾表
class Guest(models.Model):
    event=models.ForeignKey(Event)
    realname=models.CharField(max_length=64)
    phone=models.CharField(max_length=16)
    email=models.EmailField()
    sign=models.BooleanField()
    create_time=models.DateTimeField(auto_now=True)
class Meta:
    unique_together=('event','phone')
    def __str__():
        return self.realname
    

    
    

