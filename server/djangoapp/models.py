from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Dodajte ostala polja koja želite uključiti u model CarMake

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type_choices = (
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    )
    car_type = models.CharField(max_length=10, choices=type_choices)
    year = models.DateField()
    # Dodajte ostala polja koja želite uključiti u model CarModel

    def __str__(self):
        return self.name
