
from pyexpat.errors import messages
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from app.models import Category,Products,Contact_us,Sub_Category,Cart,Order,Address,wishItem,Restaurant,Coupon_Code, Review
from app.forms import  AddressForm,ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from cart.cart import Cart
from django import forms
from django.contrib.auth.decorators import login_required
from app.models import UserCreateForm
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail



client = razorpay.Client(auth=(settings.RAZORPY_KEY_ID, settings.RAZORPAY_KEY_SECRECT))

def Master(request):
    return render(request,'master.html')

def Index(request):
    category = Category.objects.all()
    products = Products.objects.all()
    #subcategory = Sub_Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.objects.filter(sub_category = categoryID).order_by('-id')
    else:
        products = Products.objects.all()
    context = {
        'category' : category,
        #'subcategory' : subcategory,
        'products' : products,
    }
    
    return render(request,'index.html',context)

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            messages.success(request,'You are successfully register!')  
            return redirect('index')
    else:
        form = UserCreateForm()
    context = {
        'form' : form,
    }    

    return render(request,'registration/signup.html',context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect('index')


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")




@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    user = request.user
    invalid_coupon = None
    valid_coupon = None
    coupon = None    
    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')    
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code = coupon_code)
                valid_coupon = "Are Applicable on current Order"
            except:
                invalid_coupon = "Invalid coupon code !"
    addresses = Address.objects.filter(user=user)      
    context = {
        'coupon' : coupon,
        'valid_coupon' : valid_coupon,
        'invalid_coupon' : invalid_coupon,
        'addresses': addresses,
      
    }    
    messages.success(request,'Item successfully add in cart!')       
    return render(request, 'cart/cart_detail.html',context)


def password_reset(request):
    return render(request, 'accounts/password_reset.html')        


def Contact_Page(request):
    if request.method == "POST":
      
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
       
       
        messages.success(request,'Your message successfully send!')
   
             
    return render(request,'contact.html')

@login_required(login_url="/accounts/login/")
def CheckOut(request):
        
       
        
        payment = client.order.create({
            "amount" : 5000,
            "currency": "INR",
            "payment_capture" : "1"
        }
        )
  
        order_id = payment['id']
        context = {
            'order_id' : order_id,
            'payment' : payment,
            
        }
       
        return render(request,'cart/checkout.html',context)
    

def Search(request):
    query = request.GET['query']

    products = Products.objects.filter(name__icontains = query)
    context = {
        'products' : products,

    }
    return render(request,'search.html',context)  

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)

    order = Order.objects.filter(user = user)
    context = {
        'order' : order,
    }
    return render(request,'order.html',context)    

def About_Page(request):
    return render(request,'about.html')


def Product_Page(request):
    category = Category.objects.all()
    products = Products.objects.all()
    context = {
        'category': category,
        'products': products,
    }
    return render(request,'product.html',context)

def Product_Detail(request,id):
    products = Products.objects.filter(id = id).first()
    related_products = Products.objects.exclude(id=products.id).filter(category=products.category)
    context = {
               'products' : products,
               'related_products': related_products,
    } 
    return render(request,'product_detail.html',context)

def HtmlFile(request):
    return render(request,'cart/htmlfile.html')

#def my_dashboard(request):
  #  return render (request, 'user/dashboard.html')    


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'user/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state ,)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('/my-dashboard/')
    
@login_required
def my_dashboard(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')

        print(profile_pic)
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user/dashboard.html', {'addresses':addresses, 'orders':orders})   

def PLACE_ORDER(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        print(str(quantity))
        image = request.POST.get('image')
        amount = request.POST.get('amount')
        # print(int(amount))
        context = {
            'order_id' : order_id,
        }
        for i in cart :
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
        
            
            # amount=amount
            # print(amount)
            total = a * b
            en = Order( 
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],      
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                payment_id = order_id,
                firstname = firstname,
                amount = amount,
                lastname = lastname,
                country = country,
                state = state,
                city = city,
                total = total,
                email = email,
          
            )
        en.save()     
        #request.session['cart'] = {}   
         
    return render(request,'order.html',context) 

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()    
    return render(request,'cart/thank-you.html')


def wishlist(request):
    wish_items = wishItem.objects.filter(user=request.user)

    context = {
           'wish_items' : wish_items,

    }
    return render(request,'wishlist.html',context)

def My_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)
    order = Order.objects.filter(user = user)
    context = {
        'order' : order,
    }
    return render(request,'my_order.html',context)

def Update_Profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password != None and password !=  "":
            user.set_password(password)
        user.save()  
        messages.success(request,'Your profile is updated successfully!')
    return render(request,'user/updateprofile.html')

def UPD(request):
    return redirect('user/updateprofile.html')

def Review_rate(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = Review.objects.get(user_id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'thank you for your review update')
            return redirect(url)


        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rate = form.cleaned_data['rate']
                data.comment = form.cleaned_data['comment']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'thank you for your review submited')
               
       
        

    return redirect(url)  







