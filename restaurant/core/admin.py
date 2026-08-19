# from django.contrib import admin
# from .models import Category,Momo
# # Register your models here.
# admin.site.register(Category)
# @admin.register(Momo)
# class MomoAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'is_available', 'created_at', 'update_at')
#     list_filter = ('category', 'is_available')
#     search_fields = ('name', 'desc')

# from django.contrib import admin
# from .models import (
#     Message,
#     Category,
#     Momo,
#     Review,
#     Contact,
#     Newsletter,
#     CateringRequest,
#     PrivateDiningBooking,
#     WorkshopBooking,
# )


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("title",)
#     search_fields = ("title",)


# @admin.register(Momo)
# class MomoAdmin(admin.ModelAdmin):
#     list_display = ("name", "category", "price", "is_available", "created_at", "update_at")
#     list_filter = ("category", "is_available")
#     search_fields = ("name", "desc")


# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ("name", "email", "phone")
#     search_fields = ("name", "email", "phone", "message")


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ("name", "order", "rating")
#     list_filter = ("rating",)
#     search_fields = ("name", "order", "message")


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ("name", "subject", "email", "phone", "newsletter", "created_at")
#     list_filter = ("subject", "newsletter", "created_at")
#     search_fields = ("name", "email", "phone", "message")


# @admin.register(Newsletter)
# class NewsletterAdmin(admin.ModelAdmin):
#     list_display = ("email", "subscribed_at")
#     search_fields = ("email",)


# @admin.register(CateringRequest)
# class CateringRequestAdmin(admin.ModelAdmin):
#     list_display = ("event_type", "event_date", "guests_range", "preferred_package", "created_at")
#     list_filter = ("event_type", "preferred_package", "event_date")
#     search_fields = ("event_type", "additional_requirements")


# @admin.register(PrivateDiningBooking)
# class PrivateDiningBookingAdmin(admin.ModelAdmin):
#     list_display = ("occasion", "date", "time_slot", "guests")
#     list_filter = ("occasion", "date", "time_slot")
#     search_fields = ("occasion", "special_requests")


# @admin.register(WorkshopBooking)
# class WorkshopBookingAdmin(admin.ModelAdmin):
#     list_display = ("workshop_type", "preferred_date", "time_preference", "number_of_participants", "created_at")
#     list_filter = ("workshop_type", "preferred_date", "time_preference")
#     search_fields = ("workshop_type", "participant_details")

# using extra css 
from django.contrib import admin
from .models import (
    Message,
    Category,
    Momo,
    Review,
    Contact,
    Newsletter,
    CateringRequest,
    PrivateDiningBooking,
    WorkshopBooking,
)


class BaseAdmin(admin.ModelAdmin):
    """Optional: Inherit from this to load custom CSS on specific model pages"""
    class Media:
        css = {
            "all": ("css/jazzmin_custom.css",)
        }


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Momo)
class MomoAdmin(BaseAdmin):
    list_display = ("name", "category", "price", "is_available", "created_at", "update_at")
    list_filter = ("category", "is_available")
    search_fields = ("name", "desc")


@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone", "message")


@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ("name", "order", "rating")
    list_filter = ("rating",)
    search_fields = ("name", "order", "message")


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ("name", "subject", "email", "phone", "newsletter", "created_at")
    list_filter = ("subject", "newsletter", "created_at")
    search_fields = ("name", "email", "phone", "message")


@admin.register(Newsletter)
class NewsletterAdmin(BaseAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)


@admin.register(CateringRequest)
class CateringRequestAdmin(BaseAdmin):
    list_display = ("event_type", "event_date", "guests_range", "preferred_package", "created_at")
    list_filter = ("event_type", "preferred_package", "event_date")
    search_fields = ("event_type", "additional_requirements")


@admin.register(PrivateDiningBooking)
class PrivateDiningBookingAdmin(BaseAdmin):
    list_display = ("occasion", "date", "time_slot", "guests")
    list_filter = ("occasion", "date", "time_slot")
    search_fields = ("occasion", "special_requests")


@admin.register(WorkshopBooking)
class WorkshopBookingAdmin(BaseAdmin):
    list_display = ("workshop_type", "preferred_date", "time_preference", "number_of_participants", "created_at")
    list_filter = ("workshop_type", "preferred_date", "time_preference")
    search_fields = ("workshop_type", "participant_details")