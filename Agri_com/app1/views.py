from decimal import Decimal
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import*
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
from .forms import*
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def index(request):
    product_list=Product.objects.all().select_related('seller')
    workers=Worker.objects.all()
    dict_products= {
        'products':product_list,
        'workers':workers
    }
    
    

    return render(request,'index.html',dict_products)
def user_home(request):
    product_list=Product.objects.all().select_related('seller')
    workers=Worker.objects.all()
    dict_products= {
        'products':product_list,
        'workers':workers,
    }
    
   
    return render(request,'user_home.html',dict_products) 
def product_list(request):
    product_list=Product.objects.all().select_related('seller')
 
    dict_products= {
        'products':product_list,
       
    }

    return render(request,'product_list.html',dict_products)
def worker_list(request):
    worker_list=Worker.objects.all()
 
    dict_products= {
        'workers':worker_list,
       
    }

    return render(request,'worker_list.html',dict_products)
def worker_orders(request):
    user_id = request.session.get('U_id') 
    user = User.objects.get(id=user_id)
    orders = Hire.objects.filter(user=user).select_related('worker')

    return render(request, 'worker_orders.html', {'orders': orders})
def failed(request):
    
    return render(request,'failed.html')
def passfailed(request):
    
    return render(request,'passfailed.html')
def success(request):
    
    return render(request,'success.html')
def sign_in(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST['email']
        phone_number = request.POST.get('phone_number')
        address = request.POST['address']
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        user_verification = User.objects.filter(email=email).exists()
        pass_verification = password == confirm_password

        if user_verification and pass_verification:
            return render(request, 'failed.html')
        else:
            if pass_verification:
                registration = User(
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    address=address,
                    password=password
                )
                registration.save()
                request.session['U_id'] = registration.id
               

                return redirect('user_home')  # or use render() if showing a template
            else:
                return render(request, 'passfailed.html')

                
            
    
    return render(request,'signin.html')
from django.shortcuts import render, redirect
from .models import User  # Make sure your User model is imported

def sign_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email, password=password).exists():
            user_dtls = User.objects.get(email=email, password=password)
            request.session['U_id'] = user_dtls.id
            request.session['U_name'] = user_dtls.name
            request.session['U_email'] = user_dtls.email
            request.session['U_phone_numbe'] = user_dtls.phone_number
            request.session['U_user'] = 'User'
            return redirect('user_home')  # Redirect to the desired page after login
       
        else:
            return render(request,'sign_page.html', {'status': 'Invalid username or password'})

    return render(request,'sign_page.html')


def logout(request):
    session_key=list(request.session.keys())
    for key in session_key:
        del request.session[key]
    return redirect(index)
 

 
def sell_page(request):
    temp = request.session.get('U_id')
    if not temp:
        return redirect('login')  # or handle not-logged-in case

    seller = get_object_or_404(Seller, id=temp)

    if request.method == 'POST':
        p_name = request.POST.get('p_name')
        categories = request.POST.get('categories')
        price = float(request.POST.get('price'))
        stock = int(request.POST.get('stock'))
        description = request.POST.get('description')
        image_url = request.FILES.get('image_url')

        if image_url:
            fs = FileSystemStorage()
            filename = fs.save(image_url.name, image_url)

            # Save product
            product = Product(
                seller=seller,
                p_name=p_name,
                categories=categories,
                price=price,
                stock=stock,
                description=description,
                image_url=filename  # if your model uses FileField/ImageField
            )
            product.save()

            return redirect('seller_area')

    return render(request, 'sell_page.html')
# def product_list(request):

#     return render(request, 'seller_area.html')  
def seller_area(request):
    temp=request.session['U_id']
    seller=Seller.objects.get(id=temp)
   
    product_list=Product.objects.filter(seller=seller)
    product_Image=Product_Image.objects.filter(product__in=product_list)
    dict_products= {
        'products':product_list,
        'product_Image':product_Image,
    }

    return render(request, 'seller_area.html',dict_products) 
def seller_reg(request):
    temp=request.session['U_id']
    if Seller.objects.filter(seller=temp).exists():
        return redirect('seller_area') 
  
    if request.method == 'POST':
        check_U=User.objects.get(id=temp)
        name=request.POST.get('name')
        phone_number=request.POST.get('phone_number')
        business_type=request.POST.get('business_type')
        seller_save=Seller(
            seller=check_U,
            name=name,
            phone_number=phone_number,
            business_type=business_type,
        )
        seller_save.save()
        return redirect('seller_area')
    else:

        return render(request, 'seller_reg.html')
     
def productEdit(request,id):
   
    product_id=Product.objects.get(id=id)
    if request.method == 'POST':
        product_id.p_name = request.POST.get('p_name')
        product_id.categories = request.POST.get('categories')
        product_id.price = float(request.POST.get('price'))
        product_id.stock = int(request.POST.get('stock'))
        product_id.description = request.POST.get('description')

        image = request.FILES.get('image_url')  # Use get() to avoid error

        if image:
            f = FileSystemStorage()
            filename = f.save(image.name, image)
            product_id.image_url = f.url(filename)

        product_id.save()
        return redirect('seller_area') 
    else:

         return render(request, 'product_edit.html',{'product':product_id}) 

       
def product_delete(request,id):
    product_id=Product.objects.get(id=id)
    product_id.delete()
    return redirect('seller_area')
       
def seller_profile(request):
    temp=request.session['U_id']
    check_U=User.objects.get(id=temp)
    seller=Seller.objects.get(id=temp)
    
    return render(request, 'seller_ profile.html',{'seller':seller,'check_U':check_U})
def seller_profile_edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        seller_id = request.session.get('U_id')
        seller = Seller.objects.get(id=seller_id)

        if field == 'name':
            seller.name = value
        elif field == 'phone':
            seller.phone_number = value
        elif field == 'business_type':
            seller.business_type = value
        seller.save()
       
        return JsonResponse({'status': 'success','image_url': seller.profile_image.url})
    
    return JsonResponse({'status': 'failed'})
def seller_profile_image_upload(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        seller_id = request.session.get('U_id')
        seller = Seller.objects.get(id=seller_id)
        seller.profile_image = request.FILES['profile_image']
        seller.save()
        return JsonResponse({'status': 'success', 'image_url': seller.profile_image.url})
    
    return JsonResponse({'status': 'error'})
def user_profile(request):
    temp=request.session['U_id']
    check_U=User.objects.get(id=temp)
    
    
    return render(request, 'user_profile.html',{'check_U':check_U})
def user_profile_edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        user_id = request.session.get('U_id')
        user = User.objects.get(id=user_id)

        if field == 'name':
            user.name = value
        elif field == 'phone':
            user.phone_number = value
        elif field == 'email':
            user.email = value
        elif field == 'address':
            user.address = value
        user.save()
       
        return JsonResponse({'status': 'success','image_url': user.user_img.url})
    
    return JsonResponse({'status': 'failed'})
def user_profile_image_upload(request):
    if request.method == 'POST' and request.FILES.get('user_img'):
        user_id = request.session.get('U_id')
        user = User.objects.get(id=user_id)
        user.user_img = request.FILES['user_img']
        user.save()
        return JsonResponse({'status': 'success', 'image_url': user.user_img.url})
    
    return JsonResponse({'status': 'error'})
def worker_reg(request):
    temp=request.session['U_id']
    if Worker.objects.filter(user=temp).exists():
        return render(request,'worker_dashboard.html')
    if request.method == 'POST':
        check_U=User.objects.get(id=temp)
        name=request.POST.get('name')
        age=request.POST.get('age')
        work_category=request.POST.get('work_category')
        work_name=request.POST.get('work_name')
        price_type=request.POST.get('price_type')
        price=request.POST.get('price')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')
        worker_save=Worker(
            user=check_U,
            name=name,
            age=age,
            work_category=work_category,
            work_name=work_name,
            price_type=price_type,
            price=price,
            phone=phone,
            email=email,
            address=address,
            
        )
        worker_save.save()
        
        return redirect('worker_dashboard')
    
    

    return render(request, 'worker_reg.html', )
def worker_dashboard(request):
    user_id = request.session.get('U_id')  # safer than direct ['U_id']
    user = User.objects.get(id=user_id)
    worker = Worker.objects.get(user=user)
    # Check if the user is a worker
    if not worker:  # or handle the case where the worker doesn't exist
        return redirect('worker_reg')
           
    
    works = Hire.objects.filter(worker=worker).select_related('user')

    return render(request, 'worker_dashboard.html', {'works': works})


def image_upload(request):
    user=request.session['U_id']
    worker=Worker.objects.get(user=user)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            worker_image = Worker_image(
                Worker=worker,
                images=image
            )
            worker_image.save()
        return redirect('image_upload') 
    images = Worker_image.objects.filter(Worker=worker)
    

    return render(request, 'image_upload.html', {'images': images})
def image_delete(request,id):
    image_id=Worker_image.objects.get(id=id)
    image_id.delete()
    return redirect('image_upload')
def worker_profile(request):
    user=request.session['U_id']
    worker=Worker.objects.get(user=user)    
    dict_worker={
        'worker':worker,
    }
    
    return render(request,'worker_profile.html',dict_worker)
def worker_profile_edit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        worker_id = request.session.get('U_id')
        worker = Worker.objects.get(id=worker_id)

        if field == 'name':
            worker.name = value
        elif field == 'phone':
            worker.phone = value
        elif field == 'work_category':
            worker.work_category = value
        elif field == 'work_name':
            worker.work_name = value
        elif field == 'price_type':
            worker.price_type = value
        elif field == 'price':
            worker.price = value
        elif field == 'email':
            worker.email = value
        elif field == 'address':
            worker.address = value
        elif field == 'work_experience':
            worker.experience = value
        
        worker.save()
       
        return JsonResponse({'status': 'success','image_url': worker.image.url})
    
    return JsonResponse({'status': 'failed'})
def worker_profile_image_upload(request):
    if request.method == 'POST':
        worker_id = request.session.get('U_id')
        worker = Worker.objects.get(id=worker_id)
        worker.image = request.FILES['image']
        worker.save()
        return JsonResponse({'status': 'success', 'image_url': worker.image.url})
    
    return JsonResponse({'status': 'error'})    
def user_worker_hire(request,id):
    
    worker=Worker.objects.get(id=id)
    image=Worker_image.objects.filter(Worker=worker)

    
    return render(request,'user_worker_hire.html',{'worker':worker,'image':image})
def hire_page(request, id):
    worker = Worker.objects.get(id=id)
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    address = Address.objects.filter(user=check_U)
    if request.method == 'POST':
        worker_count = request.POST.get('worker_count')
        address_id = request.POST.get('selected_address')
        phone_number=request.POST.get('phone_number')
        address = Address.objects.get(id=address_id)
        hire = Hire(
            worker=worker,
            user=check_U,
            worker_count=worker_count,
            address=address,
            phone_number=phone_number,
        )

        hire.save()
        return redirect('After_hire')  # Redirect to the desired page after hiring

    return render(request, 'hire_page.html', {'worker': worker, 'check_U': check_U, 'address': address})
def address_page(request):
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    check_address = Address.objects.filter(user=check_U).exists()
    if not check_address:
        return redirect('add_address')  # Redirect to add address page if no address is found
    address = Address.objects.filter(user=check_U)

    

    return render(request,'address.html',{'check_U':check_U,'address':address})
def add_address(request):
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    if request.method == 'POST':
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        address = Address(
            user=check_U,
            address_line=address_line,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code
        )
        address.save()
        return redirect('address_page')

    return render(request, 'address.html')
def address_delete(request,id):
    user_id = request.session.get('U_id')
    user = User.objects.get(id=user_id)
    address=Address.objects.get(id=id)
    remaining_addresses = Address.objects.filter(user=user)
    was_default = address.is_default
    address.delete()

    if was_default:
        # Check if the user still has addresses
        
        if remaining_addresses.exists():
            # Set the first one as default
            first_one = remaining_addresses.order_by('id').first()
            first_one.is_default = True
            first_one.save()
    return redirect('address_page')
def address_edit(request,id):
    address=Address.objects.get(id=id)
    if request.method == 'POST':
        address.address_line = request.POST.get('address_line')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.zip_code = request.POST.get('zip_code')
        
        address.save()
        return redirect('address_page')

    return render(request, 'address_edit.html', {'address': address})
def setdefault_address(request,id):
    address=Address.objects.get(id=id)
    address.is_default=True
    address.save()
    # Set all other addresses to not default
    Address.objects.exclude(id=id).filter(user=address.user).update(is_default=False)
  
        
    
    # Redirect to the address page or any other page as needed


    return redirect('address_page')

def select_hire_status(request,id):
    if request.method == 'POST':
        hire = get_object_or_404(Hire, id=id)
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            hire.status = new_status
            hire.save()
    return redirect('worker_dashboard')
def Work_history(request):
    user_id = request.session.get('U_id') 
    worker=Worker.objects.get(user=user_id)
    works = Hire.objects.filter(worker=worker).select_related('user')
    
       
    return render(request, 'work_history.html', {'works': works})
def After_hire(request):

    return render(request, 'After_hire.html')
def product_image_upload(request,id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            product_image = Product_Image(
                product=product,
                image=image
            )
            product_image.save()
        return redirect('product_image_upload', id=id)  # Redirect to the same page to see the uploaded images
    images = Product_Image.objects.filter(product=product)

    return render(request, 'product_image_upload.html', {'images': images, 'product': product})
def product_image_delete(request,id):
    image_id=Product_Image.objects.get(id=id)
    image_id.delete()
    return redirect('product_image_upload', id=image_id.product.id)  # Redirect to the product image upload page
def  product_Image(request,id):
    product = Product.objects.get(id=id)
    images = Product_Image.objects.filter(product=product)

    return render(request, 'seller_area.html', {'images': images})
def Product_view_page(request,id):
    product = Product.objects.get(id=id)
    images= Product_Image.objects.filter(product=product)
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    
    
      # Redirect to the desired page after hiring

    return render(request, 'Product_view_page.html', {'check_U': check_U, 'product': product, 'image': images})
def Buy_page(request,id):
    product = Product.objects.get(id=id)
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    address= Address.objects.filter(user=check_U)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        address_id = request.POST.get('selected_address')
        phone_number=request.POST.get('phone_number')
        total_price = request.POST.get('total_price')
        address = Address.objects.get(id=address_id)
        order = Order(
            Seller=product.seller,
            user=check_U,
            product=product,
            quantity=quantity,
            address=address,
            phone_number=phone_number,
            total_price=total_price  # Calculate total price
        )
        order.save()

        if product.stock >= int(quantity):
            product.stock -= int(quantity)
            product.save()
        return redirect('order_placed_success')
  
    return render(request, 'Buy_page.html', {'product': product, 'check_U': check_U, 'address': address})
# def order_history(request):
#     user_id = request.session.get('U_id') 
#     user = User.objects.get(id=user_id)
#     orders = Order.objects.filter(user=user).select_related('product', 'Seller')
    
       
#     return render(request, 'order_history.html', {'orders': orders})
# def order_cancel(request,id):
#     order = Order.objects.get(id=id)
#     order.status = 'canceled'
#     order.save()
#     return redirect('order_history')
def order_placed_success(request):
    return render(request, 'order_placed_success.html')
def orders_page(request):
    user_id = request.session.get('U_id') 
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user).select_related('product', 'Seller')

    
       
    return render(request, 'orders_page.html', {'orders': orders})
def history_order(request):
    user_id = request.session.get('U_id')
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user).select_related('product', 'Seller')

    return render(request, 'history_order.html', {'orders': orders})
def seller_orders(request):
    user_id = request.session.get('U_id') 
    user = User.objects.get(id=user_id)
    seller=Seller.objects.get(seller=user)
    orders = Order.objects.filter(Seller=seller).select_related('product', 'user')

    return render(request, 'seller_orders.html', {'orders': orders})
def seller_order_status_update(request, id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=id)
        new_status = request.POST.get('status')
        expected_delivery_date = request.POST.get('expected_delivery_date')
     
    

        order.status = new_status  # ✅ Always update status first

        # ✅ Only set expected_date if status is shipped or delivered
       
        if new_status in ['shipped', 'delivered', 'canceled'] and expected_delivery_date:
            expected_delivery_datetime = datetime.strptime(expected_delivery_date, "%Y-%m-%dT%H:%M")
            order.expected_delivery_date = expected_delivery_datetime

        if new_status == 'canceled':
            order.product.stock += order.quantity  # Refund stock if canceled
            order.product.save()


        order.save()
        return redirect('seller_area')  # or your target page

    return render(request, 'seller_orders.html')
from django.shortcuts import redirect

def kart_list(request):  
    user_id = request.session.get('U_id') 
    user = User.objects.get(id=user_id)
    karts = Kart.objects.filter(user=user).select_related('product')
 # Redirect to the confirmation page

    return render(request, 'kart.html', {'karts': karts})


    
       
    return render(request, 'kart.html', {'karts': karts})
def add_to_kart(request,id):
    product = Product.objects.get(id=id)
    user_id = request.session.get('U_id')
    check_U = User.objects.get(id=user_id)
    if request.method == 'POST':
        
        save_kart = Kart(
            user=check_U,
            product=product,
          
        )
        save_kart.save()
        return redirect('kart_list') 
     # Redirect to the desired page after adding to cart  
def clear_kart(request):
    user_id = request.session.get('U_id') 
    user = User.objects.get(id=user_id)
    karts = Kart.objects.filter(user=user)
    karts.delete()
    return redirect('user_home')  # Redirect to the cart page after clearing

def remove_from_kart(request,id):
    kart_item = Kart.objects.get(id=id)
    kart_item.delete()
    return redirect('kart_list')  # Redirect to the cart page after removal



def order_confirm(request):
    user_id = request.session.get('U_id')
    user = User.objects.get(id=user_id) 
    address = Address.objects.filter(user=user)

    selected_products = []
    total_price = Decimal('0.0') 

    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_products')
        for kart_id in selected_ids:
            kart = Kart.objects.get(id=kart_id, user=user)  # safer with user filter
            total_price += kart.quantity * kart.product.price  # ✅ Correct usage

            # Update quantity if provided
            qty_str = request.POST.get(f'quantity_{kart_id}')
            if qty_str and qty_str.isdigit():
                kart.quantity = int(qty_str)
                kart.save()

    selected_products = Kart.objects.filter(id__in=selected_ids, user=user).select_related('product')

    return render(request, 'order_confirm.html', {
        'address': address,
        'selected_products': selected_products,
        'total_price': total_price,
    })
def place_order(request):
    if request.method == 'POST':
        user_id = request.session.get('U_id')
        user = User.objects.get(id=user_id)
        selected_ids = request.POST.getlist('selected_products')
        address_id = request.POST.get('selected_address')
        address = Address.objects.get(id=address_id)
        phone_number = request.POST.get('phone_number')
        
        for kart_id in selected_ids:
            kart = Kart.objects.get(id=kart_id, user=user)
            order = Order(
                Seller=kart.product.seller,
                user=user,
                product=kart.product,
                quantity=kart.quantity,
                address=address,
                phone_number=phone_number,
                total_price=kart.quantity * kart.product.price  # Calculate total price
            )
            order.save()
            # Update product stock
            kart.product.stock -= kart.quantity 
            kart.product.save()
            # Remove from kart after placing order
        kart.delete()

      
        return redirect('order_success')
    
 

    return render(request, 'order_confirm.html', {
      
    })


def order_success(request):
    return render(request, 'order_success.html') 
def search(request):
    query = request.GET.get('query')
    products = Product.objects.none()
    workers = Worker.objects.none()

    if query:
        if query.lower() == 'worker':
            workers = Worker.objects.all()
        elif query.lower() == 'product':
            products = Product.objects.all().select_related('seller')
        else:
            products = Product.objects.filter(p_name__icontains=query).select_related('seller')
            workers = Worker.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all().select_related('seller')
        workers = Worker.objects.all()

    return render(request, 'user_home.html', {'products': products, 'workers': workers})
def contact_us(request):
    user=request.session.get('U_id')
    check_U=User.objects.get(id=user)

    return render(request, 'contact us.html',{'check_U':check_U})














    
   
    

      



   

    


