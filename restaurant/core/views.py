from django.shortcuts import render,redirect
from .models import Message,Category,Momo
from django.contrib import messages
# Create your views here.
def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')
    if cateid:
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
    return render(request,'core/menu.html')

def services(request):
    return render(request,'core/services.html')


def testemonial(request):
    return render(request,'core/testemonial.html')

def help(request):
    return render(request,'core/help.html')

def terms(request):
    return render(request,'core/terms.html')

def privacy(request):
    return render(request,'core/privacy.html')
