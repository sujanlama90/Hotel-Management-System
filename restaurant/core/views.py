from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'core/index.html')

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
