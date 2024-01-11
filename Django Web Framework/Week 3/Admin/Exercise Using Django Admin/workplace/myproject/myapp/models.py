from django.db import models

# Create your models here.
class Employees(models.Model):
    first_name= models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    role = models.CharField(max_length=200)
    shift = models.IntegerField()

    def __str__(self):
        return f"({self.first_name}, {self.last_name}, {self.role}, {self.shift})"