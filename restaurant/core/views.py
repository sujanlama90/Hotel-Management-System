from django.shortcuts import render,redirect
from .models import Message,Category,Momo,Review
from django.contrib import messages
import qrcode
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
