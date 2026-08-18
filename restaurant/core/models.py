from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categoryImages',null=True)

    def __str__(self):
        return self.title

class Momo(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    desc = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='momoImage')
    is_available = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    order = models.CharField(max_length=200)
    rating =models.PositiveSmallIntegerField()

class Contact(models.Model):

    SUBJECT_CHOICES = [
        ("reservation", "Table Reservation"),
        ("catering", "Catering Inquiry"),
        ("feedback", "Feedback/Suggestion"),
        ("complaint", "Complaint"),
        ("partnership", "Business Partnership"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200,choices=SUBJECT_CHOICES)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CateringRequest(models.Model):
    EVENT_TYPE_CHOICES = [
        ("Wedding", "Wedding"),
        ("Birthday Party", "Birthday Party"),
        ("Corporate Event", "Corporate Event"),
        ("Family Gathering", "Family Gathering"),
        ("Other Celebration", "Other Celebration"),
    ]

    GUEST_RANGE_CHOICES = [
        ("20-50", "20-50 People"),
        ("51-100", "51-100 People"),
        ("101-200", "101-200 People"),
        ("201-500", "201-500 People"),
        ("500+", "500+ People"),
    ]

    PACKAGE_CHOICES = [
        ("Basic", "Basic (रु 500/person)"),
        ("Premium", "Premium (रु 800/person)"),
        ("Custom", "Custom (Contact for Quote)"),
    ]

    event_type = models.CharField(max_length=100, choices=EVENT_TYPE_CHOICES)
    guests_range  = models.CharField(max_length=100,choices=GUEST_RANGE_CHOICES)
    event_date = models.DateField()
    preferred_package = models.CharField(max_length=100,choices=PACKAGE_CHOICES)
    additional_requirements = models.TextField(blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_type} - {self.event_date}"


class PrivateDiningBooking(models.Model):
    TIME_SLOT_CHOICES = [
        ("12:00 PM - 4:00 PM", "12:00 PM - 4:00 PM"),
        ("5:00 PM - 9:00 PM", "5:00 PM - 9:00 PM"),
        ("6:00 PM - 10:00 PM", "6:00 PM - 10:00 PM"),
        ("7:00 PM - 11:00 PM", "7:00 PM - 11:00 PM"),
    ]

    OCCASION_CHOICES = [
        ("Business Meeting", "Business Meeting"),
        ("Family Celebration", "Family Celebration"),
        ("Birthday Party", "Birthday Party"),
        ("Anniversary", "Anniversary"),
        ("Other", "Other"),
    ]

    date = models.DateField()
    time_slot = models.CharField(max_length=100,choices=TIME_SLOT_CHOICES)
    guests = models.PositiveSmallIntegerField()
    occasion = models.CharField(max_length=100,choices=OCCASION_CHOICES)
    special_requests = models.TextField()


class WorkshopBooking(models.Model):

    WORKSHOP_TYPE_CHOICES = [
        ("Momo Making Masterclass","Momo Making Masterclass"),
        ("Traditional Thali Workshop","Traditional Thali Workshop"),
        ("Nepali Street Food Special","Nepali Street Food Special"),
        ("Custom Group Workshop","Custom Group Workshop"),
    ]

    TIME_PREFERENCE_CHOICES = [
        ("10:00 AM - 1:00 PM","10:00 AM - 1:00 PM"),
        ("2:00 PM - 5:00 PM","2:00 PM - 5:00 PM"),
        ("6:00 PM - 9:00 PM","6:00 PM - 9:00 PM"),
    ]

    workshop_type = models.CharField(max_length=100, choices=WORKSHOP_TYPE_CHOICES )
    preferred_date = models.DateField()
    number_of_participants = models.PositiveIntegerField( validators=[  MinValueValidator(1), MaxValueValidator(12),])
    time_preference = models.CharField(max_length=30, choices=TIME_PREFERENCE_CHOICES, blank=True)
    participant_details = models.TextField( blank=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return (
            f"{self.workshop_type} - "
            f"{self.preferred_date} - "
            f"{self.number_of_participants} participants"
        )


 
