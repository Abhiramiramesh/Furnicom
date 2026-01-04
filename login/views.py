from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import Payment

# Create your views here.
def home(request):
    return render(request,'index.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        profile = request.FILES.get('profile')

        if not username:
            messages.error(request, 'username field required.')
            return redirect('register')
        
        elif not email:
            messages.error(request,'email is required')
            return redirect('register')
        
        elif not phoneno:
            messages.error(request,'phoneno is required')
            return redirect('register')
        
        elif not  password :
            messages.error(request,'password is required')
            return redirect('register')
        
        elif not  profile :
            messages.error(request,'profile is required')
            return redirect('register')

        if User.objects.filter(fullname=username).exists():
            messages.error(request, 'username already exist')
            return redirect('register')

                                      #feild name = variable name,.......)
        result = User.objects.create(fullname=username, email=email,phone=phoneno,password=make_password(password),profile=profile,role="customer")
        result.save()
        messages.success(request,'user successfully registered')
        return redirect('login')


    return render(request,'register.html')
    



def signin(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        user = authenticate(email=email,password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'login successfully')
            return redirect('home')
    return render(request,'login.html')


    
def signout(request):
    logout(request)
    messages.success(request,'logout successfully')
    return redirect('home')


def addproduct(request):
    if request.method == "POST":
        # productname = request.POST.get('productname')
        productprice = request.POST.get('productprice')
        profile = request.FILES.get('profile')
        result=Product.objects.create(productprice=productprice,profile=profile)
        result.save()
        messages.success(request,'product successfully added')
        
    return render(request,'addproduct.html')



def addcarpenter(request):
    if request.method == "POST":
        carpenter = request.POST.get('carpenter')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        # profile = request.FILES.get('profile')
        result=User.objects.create(fullname=carpenter,email=email,phone=phoneno, password=make_password(password),role="carpenter")
        result.save()
        
        
    return render(request,'addcarpenter.html')


def viewproduct(request):
     products = Product.objects.all()
     return render(request, 'viewproduct.html', {'product': products})


def viewproduct1(request):
     products = Product.objects.all()
     return render(request, 'viewproduct1.html', {'product': products})
     


def viewcarpenter(request):
     carpenters= User.objects.filter(role="carpenter")
     return render(request, 'viewcarpenter.html', {'carpenter': carpenters})


def editcarpenter(request,id):
    carpenter = get_object_or_404(User, id=id, role="carpenter")

    if request.method == "POST":
        carpenter.fullname = request.POST.get('carpenter')
        carpenter.email = request.POST.get('email')
        carpenter.phone = request.POST.get('phoneno')
        password = request.POST.get('password')
        if password:  # Update password only if a new one is provided
            carpenter.password = make_password(password)
        carpenter.save()
        return redirect('viewcarpenter')

    return render(request, 'editcarpenter.html', {'carpenter': carpenter})



def addcolour(request):
    if request.method == "POST":
        colourname = request.POST.get('colourname')
        image = request.FILES.get('profile')
        price = request.POST.get('price')
        result = Colour.objects.create(colourname=colourname,image=image,price=price)
        result.save()
    return render(request, 'addcolour.html')


def viewcolour(request):
     colours= Colour.objects.all()
     return render(request, 'viewcolour.html', {'colour': colours})


def addwood(request):
    if request.method == "POST":
        woodtype = request.POST.get('woodtype')
        image = request.FILES.get('profile')
        price = request.POST.get('price')
        result = Wood.objects.create(woodtype=woodtype,image=image,price=price)
        result.save()
    return render(request, 'addwood.html')


def viewwood(request):
     woods= Wood.objects.all()
     return render(request, 'viewwood.html', {'wood': woods})


def addcategory(request):
    if request.method == "POST":
        category = request.POST.get('category')
        image = request.FILES.get('profile')
        price = request.POST.get('price')
        result = Category.objects.create(category=category,image=image,price=price)
        result.save()
    return render(request, 'addcategory.html')


def viewcategory(request):
     categories= Category.objects.all()
     return render(request, 'viewcategory.html', {'category': categories})


def customisedproduct(request):
    categories = Category.objects.all()
    colours = Colour.objects.all()
    woods = Wood.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        colour_id = request.POST.get('colour')
        wood_id = request.POST.get('wood')

        # category = Category.objects.get(id=category_id)
        # colour = Colour.objects.get(id=colour_id)
        # wood = Wood.objects.get(id=wood_id)


        category = get_object_or_404(Category, id=category_id)
        colour = get_object_or_404(Colour, id=colour_id)
        wood = get_object_or_404(Wood, id=wood_id)

        total_price = category.price + colour.price + wood.price

        Customisedorder.objects.create(
            user=request.user,
            category=category,
            colour=colour,
            wood=wood,
            total_price=total_price
        )

        return redirect('customisedproduct')

    return render(request, 'customisedproduct.html', {
        'categories': categories,
        'colours': colours,
        'woods': woods,
    })


def customisedorder(request):
     orders = Customisedorder.objects.all()
     return render(request, 'customisedorderdetails.html', {'order': orders})


     
def productorder(request):
    orders = Productorder.objects.all()
    return render(request,'productorders.html',{'orders':orders})

    

def addtocart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # If product already in cart, increase quantity
    cart_item, created = Cartitem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('viewcart')

     

def viewcart(request):
    cart_items = Cartitem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)  # Sum all cart item totals
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def remove_from_cart(request, item_id):
    item = get_object_or_404(Cartitem, id=item_id, user=request.user)
    item.delete()
    return redirect('viewcart')

def delete(request,user_id):
   result = get_object_or_404(User, id=user_id)
   result.delete()     
   messages.success(request,'user successfully deleted') 
   return redirect('list')


def delete1(request,product_id):
   result = get_object_or_404(Product, id=product_id)
   result.delete()     
   messages.success(request,'user successfully deleted') 
   return redirect('viewproduct')


def checkout(request):
    # ✅ Get all cart items for the logged-in user
    cart_items = Cartitem.objects.filter(user=request.user)

    # ✅ Calculate total amount
    total = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # ✅ Save payment details
        Payment.objects.create(
            user=request.user,
            cardholder_name=name,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            amount=total
        )
        purchased_items = list(cart_items)

        for item in cart_items:
            Productorder.objects.create(
                user=request.user,
                product=item.profile,
                quantity=item.quantity,
                total_price=item.total_price()
            )

        # ✅ Clear cart after payment success
        cart_items.delete()

        return render(request, 'checkout_success.html', {'cart_items': purchased_items,'total': total})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})



def paymentdetails(request):
    payments = Payment.objects.filter(user=request.user).order_by('-paid_at')  # latest first

    return render(request,'paymentdetails.html',{'payments':payments})

