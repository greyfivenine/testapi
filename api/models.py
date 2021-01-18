from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Deal(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                 related_name='deals')
    item = models.ForeignKey('Item', on_delete=models.CASCADE,
                             related_name='deals')
    total = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return "{}, {} from {}".format(self.customer, self.item,
                                       self.date.strftime("%d.%m.%Y %H:%M:%S"))
