from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Expense(models.Model):
    TRANSPORT_CHOICES = [("電車", "Train(電車)"), ("バス", "Bus(バス)"), ("電車＋バス", "Train + Bus(電車＋バス)"), ("タクシー", "Taxi(タクシー)"), ("その他", "Other(その他)")]
    TRIP_CHOICES = [("往復", "Round Trip(往復)"), ("片道", "One Way(片道)")]

    date = models.DateField()
    transport = models.CharField(max_length=10, choices=TRANSPORT_CHOICES)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    trip_type = models.CharField(max_length=10, choices=TRIP_CHOICES)
    purpose = models.CharField(max_length=200)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.date} - {self.purpose}"

class FrequentRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="例：通勤、出張など")
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    transport = models.CharField(max_length=50)
    amount = models.IntegerField()
    purpose = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_location} ~ {self.end_location})"
