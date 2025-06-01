from django.core.management.base import BaseCommand
from ...models import User, Listing, Booking, Review, Roles, Status
from django.utils import timezone
from decimal import Decimal
import random, datetime


class Command(BaseCommand):
    help = "Seed the database with demo data"

    def handle(self, *args, **kwargs):
        # clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.all().delete()


        # Create admin
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            phone_number='1234567890',
            role=Roles.ADMIN
        )

        # Create Hosts
        hosts = []
        for i in range(1, 6):
            host = User.objects.create_user(
                username=f'hostname{i}',
                email=f'host{i}@example.com',
                password='hostpass123',
                first_name=f'Host{i}',
                last_name='Lastname',
                phone_number=f'090{i}00{i}00{i}',
                role=Roles.HOST
            )
            hosts.append(host)

        # Create listing
        listings = []
        for idx, host in enumerate(hosts):
            for j in range(1, 3): # 3 listings each
                listing = Listing.objects.create(
                    host_id=host,
                    name=f"Listing {idx*3 + j}",
                    description="A lovely place to stay.",
                    location=f"Location {idx*3 + j}",
                    pricepernight=Decimal(f"{100 + j * 10}"),
                )
                listings.append(listing)

        # Create guests
        guests = []
        for i in range(1, 6):
            guest = User.objects.create_user(
                username=f'guest{i}',
                email=f'guest{i}@example.com',
                password='guestpass123',
                first_name=f'Guest{i}',
                last_name='Last',
                phone_number=f'080000000{i}',
                role=Roles.GUEST
            )
            guests.append(guest)

        # Create Bookings and Reviews
        review_count = 0
        for guest in guests:
            reviewed = set()
            while len(reviewed) < 2:
                listing = random.choice(listings)
                if listing in reviewed:
                    continue
                reviewed.add(listing)

                # Create booking
                start = timezone.now().date() - datetime.timedelta(days=random.randint(10, 30))
                end = start + datetime.timedelta(days=3)
                Booking.objects.create(
                    listing_id=listing,
                    user_id=guest,
                    start_date=start,
                    end_date=end,
                    total_price=listing.pricepernight * 3,
                    status=Status.CONFIRMED
                )

                # create review
                Review.objects.create(
                    listing_id=listing,
                    user_id=guest,
                    rating=random.randint(3, 5),
                    comment=f"Guest {guest.first_name} review for {listing.name}",
                )
                review_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: 1 admin, 5 hosts, 5 guests, 15 listings, {review_count} reviews"
        ))
