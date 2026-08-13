from django.shortcuts import render,redirect
from .models import Message,Category,Momo,Review
from django.contrib import messages
import qrcode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout 
import re
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')
    if cateid == 'all':
        momo = Momo.objects.filter(is_available=True)
    elif cateid:
        momo = Momo.objects.filter(is_available=True,category=cateid)
    else:
        momo = Momo.objects.filter(is_available=True)
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Message.objects.create(name=name,phone=phone,email=email,message=message)
        messages.success(request,f'Hey {name} ,your message succesfully submit')

        return redirect('index')
    context ={
        'category' :category,
        'momo' :momo
    }
    return render(request,'core/index.html',context)

def about(request):
    return render(request,'core/about.html')

def contact(request):
    return render(request,'core/contact.html')

@login_required(login_url='log_in')
def menu(request):
    category = Category.objects.all()
    qr = qrcode.make('http://127.0.0.1:8000/menu/')
    qr.save("core/static/images/qr.png")
    context ={
        'category':category
    }

    return render(request,'core/menu.html',context)

def services(request):
    return render(request,'core/services.html')


def testemonial(request):
    momo = Momo.objects.all()
    testemonial = Review.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        order = request.POST.get('order')

        Review.objects.create(name=name,rating=rating,message=message,order=order)

        return redirect('testemonial')
    context = {
        'momo':momo,
        'testemonial':testemonial
    }
    return render(request,'core/testemonial.html',context)

def help(request):
    return render(request,'core/help.html')

def terms(request):
    return render(request,'core/terms.html')

def privacy(request):
    return render(request,'core/privacy.html')
'''
==============================================================================================================
==============================================================================================================
                                                Auth Part
==============================================================================================================
==============================================================================================================

'''

def register(request):
    if request.method == "POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            if  User.objects.filter(username=username).exists():
                messages.error(request,'username already exists')
                return redirect('register')
            if  User.objects.filter(email=email).exists():
                messages.error(request,'email already exists')
                return redirect('register')
            
            if not re.search(r"[A-Z]",password):
                messages.error(request,'paswword must contain at least one upper char')

            if not re.search(r"\d",password):
                    messages.error(request,'paswword must contain at least one digit')

            try:
                user = User(first_name=fname,username=username)
                validate_password(password,user=user)
                User.objects.create_user(first_name = fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,'your account successfuly register')
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
        else:
            messages.error(request,'password and confirm password doesnot match')
            return redirect('register')
    return render(request,'auth/register.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet')
            return redirect('log_in')
            
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Invalid Pasword!!')
            return redirect('register')
    return render(request,'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')