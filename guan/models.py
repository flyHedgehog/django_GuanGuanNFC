from django.db import models
import time
# Create your models here.

class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=32,unique=True,null=False)
    password = models.CharField(max_length=32,null=False)
    active_day = models.IntegerField(default=0)
    last_act = models.CharField(max_length=1000,default="1970-01-01")
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))
    def __str__(self):
        return self.user_name

class ActivityType(models.Model):
    nid = models.AutoField(primary_key=True)
    act_type = models.CharField(max_length=32,unique=True,null=False)
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class Activity(models.Model):
    nid = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nfc = models.CharField(max_length=1000,null=False)
    type_id = models.IntegerField()
    act_name = models.CharField(max_length=1000,null=False)
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class ActSta(models.Model):
    nid = models.AutoField(primary_key=True)
    act_id = models.IntegerField()
    user_id = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    moment_text = models.CharField(max_length=1000,default="")
    is_shared = models.IntegerField(default=0)
    shared_time = models.BigIntegerField()
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class Box(models.Model):
    nid = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nfc = models.CharField(max_length=1000,null=False)
    box_name = models.CharField(max_length=1000,null=False)
    box_pos = models.CharField(max_length=1000, null=False)
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class BoxContent(models.Model):
    nid = models.AutoField(primary_key=True)
    box_id = models.ForeignKey(Box,on_delete=models.CASCADE)
    thing_name = models.CharField(max_length=1000,null=False)
    thing_num = models.IntegerField()
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class Friend(models.Model):
    nid = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    friend_id = models.IntegerField()
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

class Application(models.Model):
    nid = models.AutoField(primary_key=True)
    from_id = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    to_id = models.IntegerField()
    content = models.CharField(max_length=1000,null=False,blank=False)
    is_processed = models.IntegerField(default=0)
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))


class PushNote(models.Model):
    nid = models.AutoField(primary_key=True)
    author_id = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,null=False,blank=False)
    summary = models.CharField(max_length=1000,null=False,blank=False)
    contents = models.CharField(max_length=10000,null=False,blank=False)
    created_time = models.BigIntegerField(default=int(time.time()))
    updated_time = models.BigIntegerField(default=int(time.time()))

