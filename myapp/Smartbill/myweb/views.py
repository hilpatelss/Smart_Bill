from django.shortcuts import render, redirect ,reverse
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
        else:
            success = "Customer not found"
        return HttpResponse(success)

@login_required(login_url="/signin/")
def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

@login_required(login_url="/signin/")   
def customers(request):
    user = request.user
    Cust  = Customer.objects.filter(user=user)
    cust_total = Cust.count()
    cust_revenue = 0
    cust_bills = 0
    for c in Cust:
        c.Customer_name = c.Customer_name.title()
        cust_bills += c.customer_bill_count
        cust_revenue += c.customer_bill_spent
        c.initials = c.Customer_name[0].upper() + c.Customer_name.split(" ")[-1][0].upper()

    Stats = {
        "cust_total": cust_total,
        "cust_revenue": cust_revenue,
        "cust_bills": cust_bills
    }

    context = {"page":"customers", "cust" : Cust , "Stats":Stats }
    return render(request,'customers.html',context)

@csrf_protect
@login_required(login_url="/signin/")   
def editcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get("Customer_email")
        user = request.user
        cust  = Customer.objects.filter(user=user).filter(Customer_mobile = Customer_mobile).first()
        cust.Customer_name = Customer_name
        cust.Customer_mobile = Customer_mobile  
        cust.Customer_email = Customer_email
        cust.save()
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
    
    
@csrf_protect
@login_required(login_url="/signin/")   
def addcustomer(request):
    if request.method == "POST":
        user =request.user
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get('Customer_email')
        cust = Customer.objects.create(
            user=user,
            Customer_name=Customer_name,
            Customer_mobile=Customer_mobile,
            Customer_email=Customer_email
        )
        cust.save()
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
    
@login_required(login_url="/signin/")   
def deletecustomer(request):
    if request.method == "POST":
        User = request.user
        Customer_mobile = request.POST.get("Customer_mobile")
        cust = Customer.objects.filter(user=User).filter(Customer_mobile = Customer_mobile).first()
        if cust:
            cust.delete()

        print(Customer_mobile)
        return redirect('/customers/')
    return redirect('/customers/')
 
@login_required(login_url="/signin/")
def invoice(request):
    context = {"page":"home"}
    return render(request,'invoice.html',context)

@login_required(login_url="/signin/")
def products(request):
    User = request.user
    prod = Products.objects.filter(user=User)
    prod_count = prod.count()
    Prod_inStock = 0
    Prod_outStock = 0
    prod_lowStock = 0
    for p in prod:
        p.Product_name = p.Product_name.title()
        if p.Product_stock <= 0:
            p.Product_status = "out-stock"
            p.Product_design = "badge-out"
            Prod_outStock += 1
        elif p.Product_stock < 100:
            p.Product_status = "low-stock"
            p.Product_design = "badge-low"
            prod_lowStock += 1
        else:
            p.Product_status = "in-stock"
            p.Product_design = "badge-in"
            Prod_inStock += 1
    Stats = {
        "prod_count": prod_count,
        "Prod_inStock": Prod_inStock,
        "Prod_outStock": Prod_outStock,
        "prod_lowStock": prod_lowStock
    }
    context = {"page":"home", "prod": prod, "Stats": Stats}
    return render(request,'products.html',context)

@login_required(login_url="/signin/")   
def editproducts(request):
    if request.method == "POST":
        id = request.POST.get("id")
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        prod = Products.objects.filter(user=request.user).filter(id = id).first()
        prod.Product_name = Name
        prod.Product_price = Price
        prod.Product_gst = gst
        prod.Product_stock = Stock
        prod.save()
        print(id,Name,Price,gst,Stock)
        return redirect('/products/')
    
@csrf_protect
@login_required(login_url="/signin/")   
def addproducts(request):
    if request.method == "POST":
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        prod = Products.objects.create(
            user = request.user,
            Product_name = Name,
            Product_price = Price,
            Product_stock = Stock,
            Product_gst =gst
        )
        prod.save()
        print(Name,Price,gst,Stock)
        return redirect('/products/')
    
@login_required(login_url="/signin/")   
def deleteproducts(request):
    if request.method == "POST":
        Products_id = request.POST.get("Products_id")
        User = request.user
        prod = Products.objects.filter(user=User).filter(id = Products_id).first()
        if prod:
            prod.delete()
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
    user = request.user
    biz = Business.objects.filter(user = user).first()
    format = Formet.objects.filter(user = user).first()
    context = {"page":"home", "biz": biz, "user": user ,"format":format }
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
        user = request.user
        business = Business.objects.filter(user=user).first()
        business.bizName = bizName
        business.full_address = full_address
        business.phone_number = phone_number
        business.Gstin = Gstin
        business.Pan_number = Pan_number
        business.save()
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
        user = request.user
        format = Formet.objects.filter(user=user).first()
        format.Inv_prefix = Inv_prefix
        format.Inv_footer = Inv_footer
        format.Inv_due_days = Inv_due_days
        format.Show_signature_area = True if Show_signature_area == "true" else False
        format.Show_TC = True if Show_TC == "true" else False
        format.save()
        print(Inv_prefix,Inv_footer,Inv_due_days,Show_signature_area,Show_TC)
        return redirect(reverse('settings') + '#tab-invoice')

@csrf_protect
@login_required(login_url="/signin/")   
def edituser(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        first_name, last_name = full_name.split()
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        if pass2 == "":
            user = request.user
            user.username = username
            user.first_name =first_name
            user.last_name =last_name
            user.save()
        else:
            user = request.user
            user.username = username
            user.first_name =first_name
            user.last_name =last_name
            if user == authenticate(username =username,password =pass1):
                user.set_password(pass2)
            user.save()
            return render('/settings/#tab-account')
        
        return render('/settings/#tab-account')
 
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

        formet = Formet.objects.create(
            user =user, 
        )
        formet.save()

        login(request ,user)
        return redirect('/dashboard/')
    context = {"page":"SignUp"}
    return render(request,'signup.html',context)

@login_required(login_url="/signin/")
def Signout(request):
    logout(request)
    return redirect('/signin/')


