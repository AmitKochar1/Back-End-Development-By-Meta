from django.db import models

# Create your models here.
class Booking(models.Model):
    Name = models.CharField(max_length = 255)
    No_of_guest = models.IntegerField(default = 5)
    Bookingdate = models.DateField()
    
    def __self__(self):
        return self.Name
    
class Menu(models.Model):
    Title = models.CharField(max_length = 200)
    Price = models.IntegerField()
    Inventory = models.SmallIntegerField()
    
    def __str__(self):
        return self.Title