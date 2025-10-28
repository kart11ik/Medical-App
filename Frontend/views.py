import razorpay
from django.shortcuts import render, redirect
from Frontend.models import contactdb, signupdb, cartdb, bookingdb
from ShopApp.models import productdb
from ShopApp.models import catdb
from django.contrib import messages
from django.contrib.auth.models import User



def shop_index(request):
    cat = catdb.objects.all()
    return render(request,"Shop_index.html",{'cat':cat})

def product_page(request):
    product = productdb.objects.all()
    cat = catdb.objects.all()
    return render(request,"Product.html",{'product':product , 'cat':cat})

def product_filter(request,cat_name):
    cat = catdb.objects.all()
    data = productdb.objects.filter(catname=cat_name)
    return render(request,"product_filter.html",{'data':data, 'cat':cat })

def single_product(request,pro_id):
    data = productdb.objects.get(id=pro_id)
    return render(request,"single_product.html",{'data':data})

def about_us(request):
    return render(request,"about_us.html")

def contact_us(request):
    return render(request,"contact_us.html")

def contactdata(request):
    if request.method == "POST":
        cona = request.POST.get('contactname')
        ema = request.POST.get('email')
        conum = request.POST.get('contactnumber')
        sub = request.POST.get('subject')
        sugg = request.POST.get('suggestion')
        obj = contactdb(contactname=cona,email=ema,contactnumber=conum,subject=sub,suggestion=sugg)
        obj.save()
        return redirect(contact_us)


# USER LOGIN AND SIGN UP

def signup_user(request):
    return render(request,"signup_user.html")

def signupdata(request):
    if request.method == "POST":
        fna = request.POST.get('fullname')
        mob = request.POST.get('mobile')
        ema = request.POST.get('email')
        una = request.POST.get('username')
        pas = request.POST.get('password')
        obj = signupdb(fullname=fna,mobile=mob,email=ema,username=una,password=pas)
        obj.save()
        messages.success(request, "Account Created Successfully")
        return redirect(signup_user)

def login_user(request):
    return render(request,"login_user.html")

# views.py in Frontend app

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Frontend.models import signupdb  # Corrected model from frontend app


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import signupdb  # Import your Frontend signupdb model
from django.contrib.auth.models import User  # Import Django User model for ShopApp

def Userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists in Frontend (Signupdb model)
        frontend_user = signupdb.objects.filter(username=username).first()
        if frontend_user:
            # If the user exists in Frontend, check the password
            if frontend_user.password == password:  # In real apps, always hash passwords!
                request.session['username'] = username
                messages.success(request, "Login Success")
                return redirect('shop_index')  # Redirect to ShopApp index page for frontend user
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login_user')

        # Check if the user exists in ShopApp (User model)
        shopapp_user = User.objects.filter(username=username).first()
        if shopapp_user:
            # If the user exists in ShopApp, authenticate and check password
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                if user.is_superuser:  # Check if the user is a superuser
                    messages.success(request, "Login Success")
                    return redirect('bookingsss')  # Redirect to ShopApp admin page for admin
                else:
                    messages.success(request, "Login Success")
                    return redirect('shop_index')  # Redirect to ShopApp index page for regular users
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login_user')

        else:
            messages.error(request, "User does not exist")
            return redirect('login_user')

    return render(request, 'login_user.html')  # Render the login page on GET request

# In frontend/views.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def Userlogout(request):
    # If the user is logged in as a ShopApp user
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_superuser'):  # This checks if the user is from ShopApp
            logout(request)  # Logout the ShopApp user

    # Clear the session data
    request.session.flush()

    # Redirect the user to the appropriate page after logout (e.g., login page)
    return redirect('login_user')  # Or redirect to Frontend index or ShopApp index as needed


# cart

def cart_page(request):
    data = cartdb.objects.filter(username=request.session['username'])
    total_price=0
    for i in data:
        total_price=total_price+i.totalprice
    return render(request,"Cart_page.html", {'data':data, 'total_price':total_price})


# views.py
from django.shortcuts import render
from .models import contactdb  # Assuming the model name is contactdb

def suggestion(request):
    data = contactdb.objects.all()  # Fetch all contactdb records
    return render(request, 'your_template_name.html', {'data': data})




def cartdata(request):
    if request.method == "POST":
        una = request.POST.get('username')
        pna = request.POST.get('productname')
        qua = request.POST.get('quantity')
        tpri = request.POST.get('totalprice')
        des = request.POST.get('description')
        obj = cartdb(username=una,productname=pna,quantity=qua,totalprice=tpri,description=des)
        obj.save()
        messages.success(request,"Added to Cart")
        return redirect(cart_page)

def delete_cart(request,pro_id):
    data = cartdb.objects.filter(id=pro_id)
    data.delete()
    messages.error(request,"Item deleted From cart")
    return redirect(cart_page)

def checkout_page(request):
    data = cartdb.objects.filter(username=request.session['username'])
    total_price = 0
    for i in data:
        total_price = total_price + i.totalprice
    return render(request,"Checkout.html",{'data':data , 'total_price':total_price})



def bookingdata(request):
    if request.method=="POST":
        fna =  request.POST.get('fullname')
        una =  request.POST.get('username')
        addr =  request.POST.get('address')
        cty =  request.POST.get('city')
        pin =  request.POST.get('pincode')
        mob =  request.POST.get('mobile')
        ema =  request.POST.get('email')
        prona =  request.POST.get('productname')
        ttpri = request.POST.get('totalprice')
        obj = bookingdb(fullname=fna,username=una,address=addr,city=cty,pincode=pin,mobile=mob,email=ema,productname=prona,totalprice=ttpri)
        obj.save()
        return redirect(payment_product)




def payment_product(request):

    last_object = bookingdb.objects.order_by('-id').first()
    payy = last_object.totalprice
    payy_str_hotel = str(payy)
    for ptotl in payy_str_hotel:
        print(ptotl)

    if request.method == "POST":
        amount=50000
        order_currency='INR'
        client = razorpay.Client(auth=('rzp_test_jcVIUHkalKhqwa','Gwt5sgqFhjy0ur0qJUKQxTwY'))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
    return render(request,"pay.html",{'payy_str_hotel':payy_str_hotel})

from django.shortcuts import render
from django.utils import timezone
from .models import bookingdb

def bill_view(request):
    # Fetch the last booking record
    last_object = bookingdb.objects.order_by('-id').first()

    # Prepare context data for the bill
    context = {
        'customer_name': last_object.fullname,   # Use 'fullname' field
        'product_name': last_object.productname,  # Use 'productname' field
        'quantity': 1,  # Assuming quantity is 1 unless specified elsewhere
        'total_price': last_object.totalprice,    # 'totalprice' field
        'date': timezone.now(),
    }

    # Render the bill HTML page with the context data
    return render(request, "bill.html", context)



def user_orders(request):
    # Ensure the user is logged in and their session has the 'username' key
    if 'username' in request.session:
        data = bookingdb.objects.filter(username=request.session['username'])
        context = {'data': data}
        return render(request, 'my_order.html', context)