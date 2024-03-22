from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

MAKE = (
    ("Audi", "Audi"),
    ("BMW", "BMW"),
    ("Cadillac", "Cadillac"),
    ("Chevrolet", "Chevrolet"),
    ("Ford", "Ford"),
    ("Honda", "Honda"),
    ("Hyundai", "Hyundai"),
    ("Jeep", "Jeep"),
    ("Kia", "Kia"),
    ("Land Rover", "Land Rover"),
    ("Lexus", "Lexus"),
    ("Mazda", "Mazda"),
    ("Mercedes-Benz", "Mercedes-Benz"),
    ("Nissan", "Nissan"),
    ("Porsche", "Porsche"),
    ("Subaru", "Subaru"),
    ("Tesla", "Tesla"),
    ("Toyota", "Toyota"),
    ("Volkswagen", "Volkswagen"),
    ("Volvo", "Volvo")
)

CONDITION = (
    ("Like New", "Like New"),
    ("Excellent", "Excellent"),
    ("Good", "Good"),
    ("Fair", "Fair"),
    ("Poor", "Poor"),
    ("Damaged", "Damaged"),
    ("Salvage", "Salvage"),
    ("Rebuilt", "Rebuilt"),
    ("Worn", "Worn"),
    ("Broken", "Broken"),
    ("Non-Operational", "Non-Operational"),
    ("Mint Condition", "Mint Condition"),
    ("Average", "Average"),
    ("Scratched", "Scratched"),
    ("Dented", "Dented"),
    ("Rusty", "Rusty"),
    ("Needs Repair", "Needs Repair"),
    ("As Is", "As Is"),
    ("Parts Only", "Parts Only"),
    ("Scrap", "Scrap")
)

CATEGORY = (
    ("Sedan", "Sedan"),
    ("SUV", "SUV"),
    ("Hatchback", "Hatchback"),
    ("Coupe", "Coupe"),
    ("Convertible", "Convertible"),
    ("Wagon", "Wagon"),
    ("Minivan", "Minivan"),
    ("Pickup Truck", "Pickup Truck"),
    ("Crossover", "Crossover"),
    ("Luxury", "Luxury"),
    ("Sports Car", "Sports Car"),
    ("Electric", "Electric"),
    ("Hybrid", "Hybrid"),
    ("Compact", "Compact"),
    ("Off-road", "Off-road"),
    ("Vintage", "Vintage"),
    ("Exotic", "Exotic"),
    ("Limousine", "Limousine"),
    ("Truck", "Truck"),
    ("Van", "Van")
)

SOLD = (
    ("For Sale", "For Sale"),
    ("Sold", "Sold"),
    ("Reserved", "Reserved")
)

# Create your models here.

class Car(models.Model):
    make = models.CharField(
        max_length=100,
        choices=MAKE,
        default=MAKE[0][0])
    model = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(1886), MaxValueValidator(9999)])
    milage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    previous_owners = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    condition = models.CharField(
        max_length=100,
        choices=CONDITION,
        default=CONDITION[0][0])
    date_listed = models.DateTimeField(default=timezone.now)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    sold = models.CharField(
        max_length=100,
        choices=SOLD,
        default=SOLD[0][0]
    )
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    category = models.CharField(
        max_length=100,
        choices=CATEGORY,
        default=CATEGORY[0][0])
    
    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'
    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"

class Avatar(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Avatar for user_id: {self.user_id} @{self.url}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cars = models.ManyToManyField(Car, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
    
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