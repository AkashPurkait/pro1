from django.shortcuts import render , redirect
from django.db.models import Count
from django.views import View
from . models import Product ,  Customer, Cart
from . forms import CustomerRegistrationForm , CustomerProfileForm 
from django.contrib import messages

# Create your views here.
def home (request):
    return render(request, 'app/home.html')

def about (request):
    return render(request, 'app/about.html')

class CategoryView(View):
    def get(self,request,val):
        product= Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values("title")
        return render (request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product= Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values("title")
        return render (request,"app/category.html",locals())
    

class ProductDetail(View):
    def get(self,request,pk):
        product= Product.objects.get(pk=pk)
        return render (request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form= CustomerRegistrationForm()
        return render (request,"app/customerregistration.html",locals())   


    def post(self,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your account has been Register successfully")
        else:
            messages.warning(request,"Invalid Input data")
        return render (request,"app/customerregistration.html",locals())
    
class ProfileView(View):
    def get(self,request):
        form= CustomerProfileForm()
        return render (request,"app/profile.html",locals())
    

    def post(self,request):
           form= CustomerProfileForm(request.POST)
           if form.is_valid():
               user=request.user
               name=form.cleaned_data['name']
               locality=form.cleaned_data['locality']
               city=form.cleaned_data['city']
               mobile=form.cleaned_data['mobile']
               state=form.cleaned_data['state']
               zipcode=form.cleaned_data['zipcode']

               reg= Customer (user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
               reg.save()
               messages.success(request,"profile saved successfully")
           else:
               messages.warning(request,"Invalid Input data")   
           return render (request,"app/profile.html",locals())

# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     product= Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     return  redirect ("/cart")   

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(product=product, 
                                                        user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('/cart/')
    else:
        return redirect('/signin/')

def viewCart(request):
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.quantity for item in cart_items)
        total_price=int(total_price)
        return render(request, 'app/viewCart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('/signin/')

def remove_cart(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(id=id,user=request.user)
        cart_item.delete()
        return redirect('/cart/')
    else:
        return redirect('/signin/')



    
    
   
        