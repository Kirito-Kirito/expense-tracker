from django.db import models


# Create your models here.
class Expense(models.Model):
    TRANSPORT_CHOICES = [("電車", "Train(電車)"), ("バス", "Bus(バス)")]
    TRIP_CHOICES = [("往復", "Round Trip(往復)"), ("片道", "One Way(片道)")]

    date = models.DateField()
    transport = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    trip_type = models.CharField(max_length=10, choices=TRIP_CHOICES)
    purpose = models.CharField(max_length=200)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.purpose}"
