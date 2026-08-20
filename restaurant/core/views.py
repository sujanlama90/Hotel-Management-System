from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import qrcode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
import logging
logger = logging.getLogger('django')
# Python regular expression library
# Used here to check uppercase letters and numbers in passwords
import re
# Allows us to protect pages that require the user to be logged in
from django.contrib.auth.decorators import login_required
# Django's built-in password change form
from django.contrib.auth.forms import PasswordChangeForm


# ==========================================================
#                       HOME PAGE
# ==========================================================

def index(request):

    # Get all categories from the Category table
    category = Category.objects.all()


    # Get all categories from the Review table
    review = Review.objects.all()
    # Get the category ID from the URL
    # Example: ?category=2
    cateid = request.GET.get('category')
    try:
        # If user selects "all", show all available momo items
        if cateid == 'all':
            momo = Momo.objects.filter(is_available=True)
        

        # If a specific category is selected,
        # show only momo items from that category
        elif cateid:
            momo = Momo.objects.filter(
                is_available=True,
                category=cateid
            )

        # If no category is selected,
        # show all available momo items
        else:
            momo = Momo.objects.filter(is_available=True)
    except Exception as e:
        logger.error(e,exc_info=True)
    momo = None
        
    # Check whether the form was submitted
    if request.method == "POST":

        # Get form data sent by the user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the contact message into the database
        Message.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )

        subject ='thank you for submiting message'
        message =render_to_string('core/mail.html',{'name':name,'phone':phone,'email':email,'message':message,'date':datetime.now()})
        from_email = 'sujanlama2323@gmail.com'
        recipient_list = [email]
        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)

        # Show a success message
        messages.success(
            request,
            f'Hey {name}, your message successfully submitted'
        )

        # Redirect back to the home page
        return redirect('index')

        # --------------------------------------------------
        # Example of using cookies
        # --------------------------------------------------

        # response = redirect('index')
        # response.set_cookie('name', name, max_age=3600)
        # return response

    # Data that will be sent to the HTML template
    context = {
        'category': category,
        'momo': momo,
        'review':review
    }

    # Display the home page
    return render(request, 'core/index.html', context)

@login_required(login_url='log_in')
def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Please enter an email address.")
        elif Newsletter.objects.filter(email=email).exists():
            messages.error(request, "You are already subscribed!")
        else:
            Newsletter.objects.create(email=email)
            messages.success(request,"Thank you for subscribing to our newsletter!")
            return redirect(request.META.get("HTTP_REFERER", "/"))


    return redirect('index')


# ==========================================================
#                       ABOUT PAGE
# ==========================================================

def about(request):

    # Display the about page
    return render(request, 'core/about.html')


# ==========================================================
#                       CONTACT PAGE
# ==========================================================

def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter') == 'on'

        Contact.objects.create(name=name,phone=phone,email=email,subject=subject,message=message,newsletter=newsletter)

        return redirect('contact')

    # Display the contact page
    return render(request, 'core/contact.html')


# ==========================================================
#                       MENU PAGE
# ==========================================================

# User must be logged in to access this page
@login_required(login_url='log_in')
def menu(request):

    # Get all categories
    category = Category.objects.all()

    # Create a QR code containing the menu URL
    qr = qrcode.make('http://127.0.0.1:8000/menu/')

    # Save the generated QR code inside the static images folder
    qr.save("core/static/images/qr.png")

    # Send category data to the template
    context = {
        'category': category
    }

    # Display menu page
    return render(request, 'core/menu.html', context)


# ==========================================================
#                       SERVICES PAGE
# ==========================================================

def services(request):

    # Display services page
    return render(request, 'core/services.html')


# ==========================================================
#                    TESTIMONIAL PAGE
# ==========================================================

def testemonial(request):

    # Get all momo items
    momo = Momo.objects.all()

    # Get all customer reviews
    testemonial = Review.objects.all()

    # Check whether the review form was submitted
    if request.method == "POST":

        # Get review form data
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        order = request.POST.get('order')

        # Save the review into the database
        Review.objects.create(
            name=name,
            rating=rating,
            message=message,
            order=order
        )

        # Refresh the testimonial page
        return redirect('testemonial')

    # Send data to the template
    context = {
        'momo': momo,
        'testemonial': testemonial
    }

    # Display testimonial page
    return render(request, 'core/testemonial.html', context)


# ==========================================================
#                       HELP PAGE
# ==========================================================

def help(request):

    # Display help page
    return render(request, 'core/help.html')


# ==========================================================
#                       TERMS PAGE
# ==========================================================

def terms(request):

    # Display terms and conditions page
    return render(request, 'core/terms.html')


# ==========================================================
#                     PRIVACY PAGE
# ==========================================================

def privacy(request):

    # Display privacy policy page
    return render(request, 'core/privacy.html')


def CateringRequests(request):
    if request.method == 'POST':
        event_type = request.POST.get('event_type')
        guests_range = request.POST.get('guests_range')
        event_date = request.POST.get('event_date')
        preferred_package = request.POST.get('package') 
        additional_requirements = request.POST.get('additional_requirements')

        CateringRequest.objects.create(event_type=event_type,guests_range=guests_range,event_date=event_date,preferred_package=preferred_package,additional_requirements=additional_requirements)
        messages.success(request, "Your catering request has been submitted successfully!")
        return redirect(request.META.get("HTTP_REFERER", "/"))

def privateDiningBooking(request):
    if request.method == "POST":
        date = request.POST.get('date')
        time_slot= request.POST.get('time_slot')
        guests = request.POST.get('guests')
        occasion = request.POST.get('occasion')
        special_requests = request.POST.get('special_requests')
        PrivateDiningBooking.objects.create(date=date,time_slot=time_slot,guests=guests,occasion=occasion,special_requests=special_requests)
        messages.success(request, "Your private dining booking has been submitted successfully!")

        return redirect(request.META.get("HTTP_REFERER", "/"))

def workshopBooking(request):
    if request.method == 'POST':
        workshop_type = request.POST.get('workshop_type')
        preferred_date = request.POST.get('preferred_date')
        number_of_participants = request.POST.get('number_of_participants')
        time_preference = request.POST.get('time_preference')
        participant_details = request.POST.get('participant_details')

        WorkshopBooking.objects.create(workshop_type=workshop_type,preferred_date=preferred_date,
            number_of_participants=number_of_participants,
            time_preference=time_preference,
            participant_details=participant_details)
        messages.success(request, "Your workshop booking has been submitted successfully!")


        return redirect(request.META.get("HTTP_REFERER", "/"))

# ==========================================================
#                       AUTH PART
# ==========================================================
#
# This section handles:
# - User registration
# - User login
# - User logout
# - Password changing
#
# ==========================================================


# ==========================================================
#                     USER REGISTER
# ==========================================================

def register(request):

    # Check whether the registration form was submitted
    if request.method == "POST":

        # Get registration form data
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Check whether password and confirm password match
        if password == cpassword:

            # Check whether username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')

            # Check whether email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')

            # Check whether password contains at least one uppercase letter
            if not re.search(r"[A-Z]", password):
                messages.error(request,'Password must contain at least one uppercase character')
                return redirect('register')


            # Check whether password contains at least one number
            if not re.search(r"\d", password):
                messages.error(request,'Password must contain at least one digit')

                return redirect('register')


            try:

                # Create a temporary User object
                # This object is used when validating the password
                user = User(
                    first_name=fname,
                    username=username
                )

                # Validate the password using Django's password validators
                validate_password(password, user=user)

                # Create the actual user and hash the password
                User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=username,
                    email=email,
                    password=password
                )

                # Show success message
                messages.success(
                    request,
                    'Your account successfully registered'
                )

                # Redirect to registration page
                return redirect('register')

            # If password validation fails
            except ValidationError as e:

                # Display every validation error
                for i in e.messages:
                    messages.error(request, i)

        # Passwords do not match
        else:
            messages.error(
                request,
                'Password and confirm password do not match'
            )

            return redirect('register')

    # Display registration page
    return render(request, 'auth/register.html')


# ==========================================================
#                       USER LOGIN
# ==========================================================

def log_in(request):

    # Example of reading a cookie
    # name = request.COOKIES.get('name', '')

    # Check whether login form was submitted
    if request.method == "POST":

        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Get remember-me checkbox value
        remember_me = request.POST.get('remember_me')

        # Check whether username exists
        if not User.objects.filter(username=username).exists():
            messages.error(
                request,
                'Username is not registered yet'
            )
            return redirect('log_in')

        # Check username and password
        user = authenticate(
            username=username,
            password=password
        )

        # If authentication is successful
        if user is not None:
            # Log the user into Django
            login(request, user)

            # If Remember Me is checked,
            # keep the session for 10 hours
            if remember_me:
                request.session.set_expiry(36000)

            # Otherwise, expire the session when the browser closes
            else:
                request.session.set_expiry(0)

            # Get the next URL if Django redirected the user to login
            next = request.POST.get('next')

            # Go to the next page if available,
            # otherwise go to the home page
            return redirect(
                next if next else 'index'
            )

        # Username exists but password is incorrect
        else:
            messages.error(
                request,
                'Invalid Password!!'
            )

            # Redirect user back to login page
            return redirect('register')

    # Get the next URL from the URL
    # Example: /login/?next=/menu/
    next = request.GET.get('next', '')

    # Display login page
    return render(
        request,
        'auth/login.html',
        {'next': next}
    )


# ==========================================================
#                       USER LOGOUT
# ==========================================================

def log_out(request):

    # Log the current user out
    logout(request)

    # Redirect to login page
    return redirect('log_in')


# ==========================================================
#                     PASSWORD CHANGE
# ==========================================================

# Only logged-in users can access this page
@login_required(login_url='log_in')
def password_change(request):

    # Create password change form for the current user
    form = PasswordChangeForm(user=request.user)

    # Check whether password change form was submitted
    if request.method == 'POST':

        # Create form again with submitted data
        form = PasswordChangeForm(user=request.user,data=request.POST )

        # Check whether form data is valid
        if form.is_valid():
            # Save the new password
            form.save()
            # Redirect user to login page
            return redirect('log_in')

    # Display password change page
    return render(request, 'auth/password_change.html',  {'form': form})