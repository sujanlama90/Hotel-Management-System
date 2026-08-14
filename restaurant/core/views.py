from django.shortcuts import render, redirect
from .models import Message, Category, Momo, Review
from django.contrib import messages
import qrcode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
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

    # Get the category ID from the URL
    # Example: ?category=2
    cateid = request.GET.get('category')

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
        'momo': momo
    }

    # Display the home page
    return render(request, 'core/index.html', context)


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