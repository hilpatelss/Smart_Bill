from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from django.http import JsonResponse
from django.contrib import messages
from myweb.models import *

def home(request):
    context = {"page":"home"}
    return render(request,'index.html',context)

def about(request):
    context = {"page":"home"}
    return render(request,'about.html',context)

@login_required(login_url="/signin/")
def billing(request):
    context = {"page":"home"}
    return render(request,'billing.html',context)

@csrf_protect
@login_required(login_url="/signin/")   
def getcustomer(request):
    if request.method == "POST":
        Customer_mobile = request.POST.get("Customer_mobile")
        print(Customer_mobile)
        if Customer_mobile == '9265186613' :   
            success = "Hilu patel"
        return HttpResponse(success)

@login_required(login_url="/signin/")
def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

@login_required(login_url="/signin/")   
def customers(request):
    context = {"page":"customers"}
    return render(request,'customers.html',context)

@csrf_protect
@login_required(login_url="/signin/")   
def editcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get("Customer_email")
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
    
@csrf_protect
@login_required(login_url="/signin/")   
def addcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get('Customer_email')
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
    
@login_required(login_url="/signin/")   
def deletecustomer(request):
    if request.method == "POST":
        Customer_mobile = request.POST.get("Customer_mobile")
        print(Customer_mobile)
        return redirect('/customers/')
    return redirect('/customers/')
 
@login_required(login_url="/signin/")
def invoice(request):
    context = {"page":"home"}
    return render(request,'invoice.html',context)

@login_required(login_url="/signin/")
def products(request):
    context = {"page":"home"}
    return render(request,'products.html',context)

@login_required(login_url="/signin/")   
def editproducts(request):
    if request.method == "POST":
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        print(Name,Price,gst,Stock)
        return redirect('/products/')
    
@csrf_protect
@login_required(login_url="/signin/")   
def addproducts(request):
    if request.method == "POST":
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        print(Name,Price,gst,Stock)
        return redirect('/products/')
    
@login_required(login_url="/signin/")   
def deleteproducts(request):
    if request.method == "POST":
        Customer_mobile = request.POST.get("Customer_mobile")
        print(Customer_mobile)
        return redirect('/customers/')
    return redirect('/products/')

@login_required(login_url="/signin/")
def reports(request):
    context = {"page":"home"}
    return render(request,'reports.html',context)

@login_required(login_url="/signin/")
def sales_history(request):
    context = {"page":"home"}
    return render(request,'sales_history.html',context)

@login_required(login_url="/signin/")
def settings(request):
    context = {"page":"home"}
    return render(request,'settings.html',context)

@csrf_protect
@login_required(login_url="/signin/")
def editbiz(request):
    if request.method == "POST":
        bizName = request.POST.get("bizName")
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        full_address = request.POST.get("full_address")
        Gstin = request.POST.get("Gstin")
        Pan_number = request.POST.get("Pan_number")
        print(bizName,full_name,phone_number,full_address,Gstin,Pan_number)
    return redirect('/settings/#tab-shop')

@csrf_protect
@login_required(login_url="/signin/")
def editinv(request):
    if request.method == "POST":
        Inv_prefix = request.POST.get("Inv_prefix")
        Inv_footer = request.POST.get("Inv_footer")
        Inv_due_days = request.POST.get("Inv_due_days")
        Show_signature_area = request.POST.get("Show_signature_area")
        Show_TC = request.POST.get("Show_TC")
        print(Inv_prefix,Inv_footer,Inv_due_days,Show_signature_area,Show_TC)
        return redirect('/settings/#tab-invoice')

@csrf_protect
@login_required(login_url="/signin/")   
def edituser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        print(username,full_name,pass1,pass2)
        return redirect('/settings/#tab-account')
 
@csrf_protect
def signin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        print(username,password)
        if not User.objects.filter(username = username).exists():
            messages.info(request, 'invalid Username')
            return redirect('/signin/')
        
        user = authenticate(username =username,password =password)
        
        if user is None:
            messages.info(request, 'invalid password')
            return redirect('/signin/')
        else:
            login(request ,user)
            return redirect('/dashboard/')
    context = {"page":"SignIn"}
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
            messages.info(request, 'username is alraedy register')
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
            City = City
        )
        business.save()

        login(request ,user)
        return redirect('/dashboard/')
    context = {"page":"SignUp"}
    return render(request,'signup.html',context)

@login_required(login_url="/signin/")
def Signout(request):
    logout(request)
    return redirect('/signin/')


