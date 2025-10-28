from django.shortcuts import render, redirect

from Frontend.models import contactdb, bookingdb,signupdb
from ShopApp.models import catdb, productdb

from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index_page(request):
    return render(request,"index.html")

def cat_add(request):
    return render(request,"CatAdd.html")

def catdata(request):
    if request.method == "POST":
        na = request.POST.get('name')
        des = request.POST.get('description')
        img = request.FILES['image']
        obj = catdb(name=na,description=des,image=img)
        obj.save()
        messages.success(request,"added..")
        return redirect(cat_add)

def cat_display(request):
    data = catdb.objects.all()
    return  render(request,"CatDisplay.html",{'data':data})

def cat_edit(request,dataid):
    cat = catdb.objects.get(id=dataid)
    return render(request,"CatEdit.html",{'cat':cat})

def update_cat(request,dataid):
    if request.method == "POST":
        na = request.POST.get('name')
        des = request.POST.get('description')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = catdb.objects.get(id=dataid).image
        catdb.objects.filter(id=dataid).update(name=na, description=des, image=file)
        messages.success(request,"Edited Successfully")
        return redirect(cat_display)

def delete_cat(request,dataid):
    data = catdb.objects.filter(id=dataid)
    data.delete()
    messages.error(request,"Deleted Successfully")
    return redirect(cat_display)

# product

def product_add(request):
    cat = catdb.objects.all()
    return render(request,"ProductAdd.html",{'cat':cat})

def productdata(request):
    if request.method == "POST":
        cna = request.POST.get('catname')
        pna = request.POST.get('productname')
        des = request.POST.get('description')
        pri = request.POST.get('price')
        img = request.FILES['image']
        obj = productdb(catname=cna,productname=pna,description=des,price=pri,image=img)
        obj.save()
        messages.success(request,"Product added")
        return redirect(product_add)

def product_display(request):
    data = productdb.objects.all()
    return render(request,"ProductDisplay.html",{'data':data})

def product_edit(request,dataid):
    cat = catdb.objects.all()
    pro = productdb.objects.get(id=dataid)
    return render(request,"ProductEdit.html",{'pro':pro , 'cat':cat })


def product_update(request,dataid):
    if request.method == "POST":
        cna = request.POST.get('catname')
        pna = request.POST.get('productname')
        des = request.POST.get('description')
        pri = request.POST.get('price')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = productdb.objects.get(id=dataid).image
        productdb.objects.filter(id=dataid).update(catname=cna,productname=pna ,description=des, price=pri,image=file)
        messages.success(request,"Edited successfully...")
        return redirect(product_display)

def product_delete(request,dataid):
    data = productdb.objects.filter(id=dataid)
    data.delete()
    messages.error(request,"Deleted Successfully")
    return redirect(product_display)

# ADMIN

def admin_user(request):
    return render(request,"Admin_Login.html")


# In views.py of the appropriate app (Frontend or ShopApp)



# In ShopApp/views.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_logout(request):
    # If the user is logged in as a ShopApp user
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_superuser'):  # This checks if the user is from ShopApp
            logout(request)  # Logout the ShopApp user

    # Clear the session data
    request.session.flush()

    # Redirect the user to the appropriate page after logout (e.g., login page)
    return redirect('login_user')  # Or redirect to Frontend index or ShopApp index as needed


# Contact suggestion

def contact_suggestion(request):
    data = contactdb.objects.all()
    return render(request,"contactus_suggestionDisplay.html",{'data':data})

def contact_suggestion_delete(request,del_id):
    deldata = contactdb.objects.filter(id=del_id)
    deldata.delete()
    return redirect(contact_suggestion)

# def bookingsss(request):
#     data = bookingdb.objects.all()
#     return render(request,"bookingsss.html",{'data':data})

from django.db.models import Sum, Count

def bookingsss(request):
    # Get all the booking data
    data = bookingdb.objects.all()

    # Get the total number of bookings (count)
    total_bookings = bookingdb.objects.count()

    # Get the total revenue (sum of totalprice)
    total_revenue = bookingdb.objects.aggregate(Sum('totalprice'))['totalprice__sum'] or 0

    # Render the data in the template with the additional information
    return render(request, "bookingsss.html", {
        'data': data,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue
    })
