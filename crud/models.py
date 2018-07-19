from django.db import models


class Student(models.Model):
    FirstName = models.CharField(max_length=100, unique=True)
    Lastname = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, default=None)
    Date_Of_Birth = models.CharField(max_length=250)
    Relationship_Status = models.CharField(max_length=10,unique=True)
    Gender = models.CharField(max_length=10,default=None)
    Address = models.CharField(max_length=250)
    salutation = models.CharField(max_length=50)


    class Meta:
        db_table = 'Student_Details'
