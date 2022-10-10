from email.policy import default
from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, verbose_name=_('nickname'))
    email = models.EmailField(unique=True, null=True, verbose_name=_('email'))
    bio = models.TextField(null=True)
    
    # 头像
    avatar = models.ImageField(null=True, default='avatar.svg')  
    
    USERNAME_FIELD = 'email'  # 登录方式
    REQUIRED_FIELDS = ['username']  # 必填信息

class Topic(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('topic name'))

    def __str__(self):
        return self.name
    


class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, verbose_name=_('host'))
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True, verbose_name=_('topic'))
    name = models.CharField(max_length=200, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('description')) # 可以为空
    participants = models.ManyToManyField(User, related_name='participants', blank=True, verbose_name=_('participants'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created')) # 只有第一次自动当前时间
    
    class Meta:
        # 设置排序
        ordering = ['-updated', '-created']  
    
    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_('room')) # 级联删除
    body = models.TextField(verbose_name=_('body'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created')) # 只有第一次自动当前时间
    
    # class Meta:
    # # 设置排序
    #     ordering = ['-updated', '-created']  
    
    def __str__(self):
        return self.body[0:50]