from django.db import models

# Create your models here.

class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=32,unique=True,null=False)
    password = models.CharField(max_length=32,null=False)
    created_time = models.DateTimeField(auto_now = True)
    updated_time = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.user_name

class ActivityType(models.Model):
    nid = models.AutoField(primary_key=True)
    act_type = models.CharField(max_length=32,unique=True,null=False)
    created_time = models.DateTimeField(auto_now = True)
    updated_time = models.DateTimeField(auto_now = True)

class Activity(models.Model):
    nid = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nfc = models.CharField(max_length=1000,null=False)
    type_id = models.IntegerField
    act_name = models.CharField(max_length=1000,null=False)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

class ActSta(models.Model):
    nid = models.AutoField(primary_key=True)
    act_id = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    created_time = models.DateTimeField(auto_now = True)
    updated_time = models.DateTimeField(auto_now=True)

class Box(models.Model):
    nid = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nfc = models.CharField(max_length=1000,null=False)
    box_name = models.CharField(max_length=1000,null=False)
    box_pos = models.CharField(max_length=1000, null=False)
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)

class BoxContent(models.Model):
    nid = models.AutoField(primary_key=True)
    box_id = models.IntegerField()
    thing_name = models.CharField(max_length=1000,null=False)
    thing_num = models.IntegerField()
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)


