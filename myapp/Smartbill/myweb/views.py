from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from myweb.models import *

def home(request):
    context = {"page":"home"}
    return render(request,'index.html',context)

def about(request):
    context = {"page":"home"}
    return render(request,'about.html',context)

def billing(request):
    context = {"page":"home"}
    return render(request,'billing.html',context)

@login_required()
def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

def forget_password(request):
    context = {"page":"home"}
    return render(request,'forget_password.html',context)

def invoice(request):
    context = {"page":"home"}
    return render(request,'invoice.html',context)

def products(request):
    context = {"page":"home"}
    return render(request,'products.html',context)

def reports(request):
    context = {"page":"home"}
    return render(request,'reports.html',context)

def sales_history(request):
    context = {"page":"home"}
    return render(request,'sales_history.html',context)

def settings(request):
    context = {"page":"home"}
    return render(request,'settings.html',context)

def signin(request):
    context = {"page":"home"}
    return render(request,'signin.html',context)

@csrf_protect
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name") 
        last_name = request.POST.get("last_name") 
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        bizName = request.POST.get("bizName")
        bizType = request.POST.get("bizType")
        Gstin = request.POST.get("Gstin")
        City = request.POST.get("City")

        user= User.objects.filter(username = username)
        if  user.exists() :
            messages.info(request, 'Phone Number is alraedy register')
            return redirect('/signup/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
         
        if len(Gstin) == 0:
            Gstin ="A" 

        business = Business.objects.create(
            user =user, 
            phone_number = phone_number,
            bizName = bizName,
            bizType = bizType,
            Gstin = Gstin,
            City = City,
            full_address= " ",
            Pan_number = " ",
            shop_logo = " ",
            Gst_enable = "T",
            default_gst = 0
        )
        business.save()

        login(request ,user)
        return redirect('dashboard')
    context = {"page":"home"}
    return render(request,'signup.html',context)

def customers(request):
    context = {"page":"home"}
    return render(request,'customers.html',context)

