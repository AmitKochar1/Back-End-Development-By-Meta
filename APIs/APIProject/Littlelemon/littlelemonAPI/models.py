from django.db import models

# Create your models
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.title
    
class Menuitem(models.Model):
    title = models.CharField(max_length = 255)
    price = models.DecimalField(decimal_places=2, max_digits=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, on_delete = models.PROTECT, default=1)