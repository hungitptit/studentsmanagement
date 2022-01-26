# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove ` ` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from cgi import test
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from gdstorage.storage import GoogleDriveStorage
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    
    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
    class Meta:
         
        db_table = 'UserProfile'


class Class(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, null=True, blank=True)
    user = models.ForeignKey(User,models.DO_NOTHING, db_column='UserID')
    class Meta:
         
        db_table = 'Class'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    classid = models.ForeignKey(Class,models.DO_NOTHING, db_column='ClassID')
    address = models.CharField(blank=True, max_length=150, db_column='address')
    name = models.CharField(db_column='name', max_length=255, null=True, blank=True)
    gender= models.CharField (db_column='gender', max_length=100, null=True, blank=True)
    image = models.ImageField(db_column='image', null=True, upload_to='student')
    description = models.CharField(db_column='description', blank=True, max_length=2550, null=True)
    phone = models.CharField(db_column='phone', blank=True, max_length=255, null=True)
    dob = models.DateTimeField(db_column='dob',blank=True, max_length=255, null=True)
    class Meta:
         
        db_table = 'Student'


class Subject(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, null=True, blank=True)
    class Meta:
         
        db_table = 'Subject'

class Test(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, null=True, blank=True)
    weight = models.IntegerField(db_column='weight', null=True, blank=True, default=1)
    class Meta:
        db_table = 'Test'

class Result(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    semester = models.CharField(db_column='semester', blank=True, max_length=255, null=True)
    time = models.DateTimeField(db_column='time',blank=True, max_length=255, null=True,auto_now_add=True)
    score = models.FloatField(db_column='score',blank=True, max_length=255, null=True)
    student = models.ForeignKey(Student,models.DO_NOTHING, db_column='StudentID')
    subject = models.ForeignKey(Subject,models.DO_NOTHING, db_column='SubjectID')
    testid = models.ForeignKey(Test,models.DO_NOTHING, db_column='TestID')
    class Meta:
         
        db_table = 'Result'
gd_storage = GoogleDriveStorage()
class Document(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    #uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='ML',storage=gd_storage)
    class Meta:
         
        db_table = 'Document'