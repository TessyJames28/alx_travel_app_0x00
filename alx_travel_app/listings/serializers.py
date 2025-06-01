from rest_framework import serializers
from .models import User, Listing, Review, Booking


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes user data before storing in db
    """
    class Meta:
        model = User
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializes user data before storing in db
    """
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializes user data before storing in db
    """
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes user data before storing in db
    """
    class Meta:
        model = Review
        fields = '__all__'