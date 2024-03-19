from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    milage = models.IntegerField()
    previous_owners = models.IntegerField()
    condition = models.CharField(max_length=100)
    date_listed = models.DateTimeField()
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'
    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cars = models.ManyToManyField(Car)
    
    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    # should grab current logged in user
    user_sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sent_reviews')
    # should grab current user profile
    user_receiver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='received_reviews')
    content = models.CharField(max_length=100)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.content})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'review_id': self.id})