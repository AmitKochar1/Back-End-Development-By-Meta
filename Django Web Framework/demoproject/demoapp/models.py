from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f'({self.name}, {self.price})'

# class Reservation(models.Model):
#     name = models.CharField(max_length = 200) 
#     contact = models.CharField('Phone number', max_length= 300)
#     time_log = models.TimeField()
#     count = models.IntegerField()
#     notes = models.CharField(max_length=300, blank = True)

#     def __str__(self):
#         return f'({self.name}, {self.contact}, {self.time_log}, {self.count}, {self.notes})'