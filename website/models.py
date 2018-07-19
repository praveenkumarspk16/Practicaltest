from django.db import models

# Create your models here.


class Rest_framework(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    class Meta:

        db_table = 'rest_example'

class Application(models.Model):
    FirstName = models.CharField(max_length=100, unique=True)
    Lastname = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, default=None)
    Date_Of_Birth = models.CharField(max_length=250)
    Relationship_Status = models.CharField(max_length=10,unique=True)
    Gender = models.CharField(max_length=10,default=None)
    Address = models.CharField(max_length=250,)

    class Meta:
        db_table = 'Employee_Details'

    def __str__(self):
        return self.FirstName

