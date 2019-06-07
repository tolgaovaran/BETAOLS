from django.db import models
from datetime import date, datetime, timedelta

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    origin = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    registerdate = models.DateField(default=date.today())
    password = models.CharField(max_length=255)
    phonenumber=models.IntegerField(max_length=16)
    status = models.CharField(max_length=10)
    picture = models.CharField(max_length=100)
    lastact=models.DateField(default=date.today())
    def __str__(self):
        return str(self.id)+" "+self.name + " " + self.surname


class Categories(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

class Course(models.Model):
    inst = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField()
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    picture = models.CharField(max_length=100)
    def __str__(self):
        return str(self.id)+" "+self.name

class Chapter(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    showtoggle= models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)+" "+self.name + " " + self.course.name

class Material(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, blank=False, null=False)
    matpath = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField()

class Taken(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    status = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

class TakenCourse(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)


class Chat(models.Model):
    sender=models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciver")
    message = models.TextField()
    date = models.DateTimeField()
    seen = models.CharField(max_length=10)

class CourseChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField()
    seen = models.CharField(max_length=10)

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    aspath = models.CharField(max_length=50, blank=False, null=False)
    date = models.DateField()
    status = models.IntegerField()


class Superuser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=255)
    phonenumber=models.IntegerField(max_length=16)
