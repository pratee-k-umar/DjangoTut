from django.db import models

# Create your models here.

class Student(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  email = models.EmailField()
  rollno = models.IntegerField()
  address = models.TextField(null=True, blank=True)
  
  
class Car(models.Model):
  carName = models.CharField(max_length=100)
  carSpeed = models.IntegerField(default=50)