from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.
class Roles(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'


class Status(models.TextChoices):
    """Enum for order status"""
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class User(AbstractUser):
    """
    A user model that inherits from abstract user model
    Includes additional fields not defined in abstract user model
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=14, unique=True)
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    

class Listing(models.Model):
    """
    Model to hanle proper listing
    """
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    location = models.CharField(max_length=500, null=False, blank=False)
    pricepernight = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} property with id {self.property_id}"
    

class Booking(models.Model):
    """
    Model to handle property booking by guests
    """
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='booking')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest')
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.user_id.first_name} => ID: {self.user_id}"
    

class Review(models.Model):
    """
    Model to handle guest ratings
    """
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='review')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False, blank=False
    )
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing_id', 'user_id')

    def __str__(self):
        return f"rating from {self.user_id.first_name} for {self.rating} stars"
