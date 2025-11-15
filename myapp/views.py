from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Sum, Avg, Q
from django.shortcuts import render
from django.shortcuts import render, redirect
from random import randint

from .models import *


# Create your views here.
def index(request):
    data = About.objects.filter()
    datas = Contact.objects.filter()
    return render(request, "index.html", locals())

@login_required(login_url='/admin_login/')
def dashboard(request):
    user = Register.objects.filter()
    technician = Technician.objects.filter()
    Total = Request.objects.filter()
    New = Request.objects.filter(status='Not Updated Yet')
    Completed = Request.objects.filter(status='Completed')
    Approved = Request.objects.filter(status='Approved')
    Cancelled = Request.objects.filter(status='Cancelled')
    return render(request, "dashboard.html", locals())

@login_required(login_url='/user_login/')
def user_dashboard(request):
    Total = Request.objects.filter(register__user=request.user)
    New = Request.objects.filter(status='Not Updated Yet', register__user=request.user)
    Completed = Request.objects.filter(status='Completed',register__user=request.user)
    Approved = Request.objects.filter(status='Approved',register__user=request.user)
    Cancelled = Request.objects.filter(status='Cancelled',register__user=request.user)
    return render(request, "user_dashboard.html", locals())

@login_required(login_url='/technician_login/')
def technician_dashboard(request):
    Approved = Request.objects.filter(status='Approved', technician__user=request.user)
    Completed = Request.objects.filter(status='Completed', technician__user=request.user)
    return render(request, "technician_dashboard.html", locals())

def admin_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Admin Login Successful")
                return redirect('dashboard')
            else:
                messages.success(request, "Invalid Admin")
                return redirect('login_admin')
    return render(request, "admin_login.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('user_login')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('user_dashboard')
        else:
            messages.success(request, "Invalid User")
            return redirect('user_login')
    return render(request, "user_login.html")

@login_required(login_url='/user_login/')
def user_profile(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=fullname, email=email)
        Register.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Register.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/technician_login/')
def technician_profile(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobileno = request.POST['mobileno']

        user = User.objects.filter(id=request.user.id).update(first_name=fullname, email=email)
        Technician.objects.filter(user=request.user).update(mobileno=mobileno)
        messages.success(request, "Updation Successful")
        return redirect('technician_profile')
    data = Technician.objects.get(user=request.user)
    return render(request, "technician_profile.html", locals())

def technician_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Technician Login Successful")
            return redirect('technician_dashboard')
        else:
            messages.success(request, "Invalid User")
            return redirect('technician_login')
    return render(request, "technician_login.html")

@login_required(login_url='/technician_login/')
def logout_technician(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('technician_login')

def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

@login_required(login_url='/police_login/')
def request_form(request):
    if request.method == "POST":
        brandname = request.POST['brandname']
        actype = request.POST['actype']
        accapacity = request.POST['accapacity']
        natureofproblem = request.POST['natureofproblem']
        description = request.POST['description']
        address = request.POST['address']
        dateofservice = request.POST['dateofservice']
        suitabletime = request.POST['suitabletime']
        servicenumber = random_with_N_digits(8)
        brandobj = Brand.objects.get(id=brandname)

        reg = Register.objects.get(user=request.user)
        Request.objects.create(register=reg, brand=brandobj, actype=actype, accapacity=accapacity, status="Not Updated Yet",
                               natureofproblem=natureofproblem, description=description, address=address,
                               dateofservice=dateofservice, suitabletime=suitabletime, servicenumber=servicenumber)
        messages.success(request, "Your Request has been sent successfully. Service number is" + str(servicenumber))
        return redirect('request_form')
    mybrand = Brand.objects.all()
    return render(request, "request_form.html", locals())

def delete_request(request, pid):
    data = Request.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('requestlist')

def requestlist(request):
    user = request.GET.get('technician')
    action = request.GET.get('action')
    data = Request.objects.filter()
    if action == "New":
        data = data.filter(status="Not Updated Yet")
    elif action == "Approved":
        data = data.filter(status="Approved")
    elif action == "Cancelled":
        data = data.filter(status="Cancelled")
    elif action == "Completed":
        data = data.filter(status="Completed")
    elif action == "Total":
        data = data.filter()
    if user:
        data = data.filter(register__user__id=user)
        data2 = data.filter().first()
    register = Register.objects.filter(user=request.user)
    technician = Technician.objects.filter(user=request.user)
    if request.user.is_staff:
        return render(request, "new_request1.html", locals())
    elif register:
        data = data.filter(register__user=request.user)
        return render(request, "user_new_request.html", locals())
    else:
        data = data.filter(technician=technician.first())
        return render(request, "new_request.html", locals())

def request_detail(request, pid):
    data = Request.objects.get(id=pid)
    if request.method == "POST":
        status = request.POST['status']
        remark = request.POST['remark']
        technicianid = request.POST['technicianid']
        technicianobj = Technician.objects.get(id=technicianid)
        data.technician = technicianobj
        data.status = status
        data.save()
        Trackinghistory.objects.create(status1=status, technician=technicianobj, request=data, remark=remark)
        messages.success(request, "Action Updated")
        return redirect('request_detail', pid)
    mytechnician = Technician.objects.filter()
    traking = Trackinghistory.objects.filter(request=data)
    register = Register.objects.filter(user=request.user)
    technician = Technician.objects.filter(user=request.user)
    cancel = Cancel.objects.filter(request=data)
    if request.user.is_staff:
        return render(request, "admin_request_detail.html", locals())
    else:
        return render(request, "user_request_detail.html", locals())
def request_detail1(request, pid):
    data = Request.objects.get(id=pid)
    if request.method == "POST":
        status = request.POST['status']
        remark1 = request.POST['remark1']
        servicecharge = request.POST['servicecharge']
        partcharge = request.POST['partcharge']
        othercharge = request.POST['othercharge']
        data.status = status
        data.save()
        Trackinghistory.objects.update(status=status, remark1=remark1, servicecharge=servicecharge,
                                                          partcharge=partcharge, othercharge=othercharge)
        messages.success(request, "Action Updated")
        return redirect('request_detail1', pid)
    traking = Trackinghistory.objects.filter(request=data)
    return render(request, "request_detail.html", locals())

def user_cancel_request(request, pid):
    data = Request.objects.get(id=pid)
    if request.method == "POST":
        reasonforcancel = request.POST['reasonforcancel']

        Cancel.objects.create(reasonforcancel=reasonforcancel, request=data)
        messages.success(request, "Your Request has been sent successfully")
        return redirect('request_detail', pid)
    return render(request, "user_cancel_request.html", locals())

def user_register(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        mobile = request.POST['mobile']
        email = request.POST['email']
        pwd = request.POST['password']

        user = User.objects.create_user(first_name=fullname, username=email, password=pwd)
        Register.objects.create(user=user, mobile=mobile)
        messages.success(request, "Register Successful")
        return redirect('user_login')
    return render(request, "user_register.html")

@login_required(login_url='/admin_login/')
def reg_user(request):
    data = Register.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", locals())

@login_required(login_url='/admin_login/')
def logout_admin(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('admin_login')

@login_required(login_url='/user_login/')
def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('user_login')

@login_required(login_url='/admin_login/')
def add_brand(request):
    if request.method == "POST":
        brandname = request.POST['brandname']
        brandlogo = request.FILES.get('brandlogo')

        Brand.objects.create(brandname=brandname, brandlogo=brandlogo)
        messages.success(request, "Add Successfully")
        return redirect('add_brand')
    return render(request, "add_brand.html", locals())

@login_required(login_url='/admin_login/')
def manage_brand(request):
    data = Brand.objects.filter()
    mytype = request.GET.get('brandname')
    if mytype:
        data = data.filter(brandname=mytype)
    d = {'data': data}
    return render(request, "manage_brand.html", d)

@login_required(login_url='/admin_login/')
def edit_brand(request, pid):
    if request.method == "POST":
        brandname = request.POST['brandname']
        try:
            brandlogo = request.FILES['brandlogo']
            br = Brand.objects.get(id=pid)
            br.brandlogo = brandlogo
            br.save()
        except:
            pass
        Brand.objects.filter(id=pid).update(brandname=brandname)
        messages.success(request, "Updated Successful")
        return redirect('manage_brand')
    data = Brand.objects.get(id=pid)
    return render(request, "edit_brand.html", locals())

@login_required(login_url='/admin_login/')
def delete_brand(request, pid):
    data = Brand.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('manage_brand')

@login_required(login_url='/admin_login/')
def add_technician(request):
    if request.method == "POST":
        technicianname = request.POST['technicianname']
        technicianid = request.POST['technicianid']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        address = request.POST['address']
        password = request.POST['password']
        pic = request.FILES.get('pic')

        user = User.objects.create_user(first_name=technicianname, email=email, password=password, username=technicianid)
        Technician.objects.create(user=user, mobileno=mobileno, address=address, technicianname=technicianname, pic=pic)
    return render(request, "add_technician.html", locals())

@login_required(login_url='/admin_login/')
def manage_technician(request):
    data = Technician.objects.all()
    d = {'data': data}
    return render(request, "manage_technician.html", locals())

@login_required(login_url='/admin_login/')
def edit_technician(request, pid):
    if request.method == "POST":
        technicianname = request.POST['technicianname']
        technicianid = request.POST['technicianid']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        address = request.POST['address']
        try:
            pic = request.FILES['pic']
            br = Technician.objects.get(id=pid)
            br.pic = pic
            br.save()
        except:
            pass
        Technician.objects.filter(id=pid).update(technicianname=technicianname, technicianid=technicianid,
                                             email=email, mobileno=mobileno, address=address)
        messages.success(request, "Updated Successful")
        return redirect('manage_technician')
    data = Technician.objects.get(id=pid)
    return render(request, "edit_technician.html", locals())

@login_required(login_url='/admin_login/')
def change_profile_image(request, pid):
    if request.method == "POST":
        technicianid = request.POST['technicianid']
        try:
            pic = request.FILES['pic']
            br = Technician.objects.get(id=pid)
            br.pic = pic
            br.save()
        except:
            pass
        Technician.objects.filter(id=pid).update(technicianid=technicianid)
        messages.success(request, "Updated Successful")
        return redirect('manage_technician')
    data = Technician.objects.get(id=pid)
    return render(request, "change_profile_image.html", locals())

@login_required(login_url='/admin_login/')
def delete_technician(request, pid):
    data = Technician.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('manage_technician')

@login_required(login_url='/admin_login/')
def edit_about(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['editor1']

        About.objects.filter(id=1).update(pagetitle=pagetitle, description=description)
        messages.success(request, "Updated Successful")
        return redirect('dashboard')
    data = About.objects.get(id=1)
    return render(request, "edit_about.html", locals())

@login_required(login_url='/admin_login/')
def edit_contact(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['editor1']
        email = request.POST['email']
        contactno = request.POST['contactno']

        Contact.objects.filter(id=1).update(pagetitle=pagetitle, description=description, email=email, contactno=contactno)
        messages.success(request, "Updated Successful")
        return redirect('dashboard')
    data = Contact.objects.get(id=1)
    return render(request, "edit_contact.html", locals())

@login_required(login_url='/user_login/')
def change_password(request):
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('user_login')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('change_password')

    return render(request, 'change_password.html')

@login_required(login_url='/admin_login/')
def admin_change_password(request):
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')

    return render(request, 'admin_change_password.html')

@login_required(login_url='/technician_login/')
def technician_change_password(request):
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('technician_change_password')
    return render(request, 'technician_change_password.html')

@login_required(login_url='/admin_login/')
def between_dates_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Request.objects.filter(dateofservice__gte=fromdate, dateofservice__lte=todate)
        data2 = True
    return render(request, "between_dates_report.html", locals())

@login_required(login_url='/admin_login/')
def employee_wise_report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Request.objects.filter(dateofservice__gte=fromdate, dateofservice__lte=todate)
        Completed = Request.objects.filter(status='Completed')
        Approved = Request.objects.filter(status='Approved')
        data2 = True
    technician = Technician.objects.all()
    return render(request, "employee_wise_report.html", locals())

def numOfDays(date1, date2):
    return (date2 - date1).days

from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count, Sum
@login_required(login_url='/admin_login/')
def sale_report(request):
    data = None
    fromdate = None
    todate = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        req = request.POST.get('reqtype')
        print(fromdate)
        mont1 = int(fromdate.split('-')[1])
        mont2 = int(todate.split('-')[1])
        yer1 = int(fromdate.split('-')[0])
        yer2 = int(todate.split('-')[0])
        monthli = [i for i in range(mont1, mont2+1)]
        yearli = [i for i in range(yer1, yer2+1)]
    return render(request, "sales_report.html",locals())

@login_required(login_url='/technician_login/')
def technician_report(request):
    data = None
    data2 = None
    technician = Technician.objects.get(user=request.user)
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Request.objects.filter(technician=technician, dateofservice__gte=fromdate, dateofservice__lte=todate)
        data2 = True
    return render(request, "technician_report.html", locals())

@login_required(login_url='/admin_login/')
def admin_search_request(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']

        data2 = True
        data = Request.objects.filter(Q(servicenumber__icontains=fromdate))
    return render(request, "admin_search.html", locals())

@login_required(login_url='/technician_login/')
def technician_search_request(request):
    data = None
    data2 = None
    technician = Technician.objects.get(user=request.user)
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Request.objects.filter(Q(technician=technician, servicenumber__icontains=fromdate))
    return render(request, "technician_search.html", locals())
