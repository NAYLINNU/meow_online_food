from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .context_processors import get_cart_amounts, get_cart_counter

from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)#Take care double underscore front is_active
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items= None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            #Check if the food item exit

            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    checkcart =Cart.objects.get(user=request.user, fooditem = fooditem )
                    #Increace  the cart quantity
                    checkcart.quantity += 1
                    checkcart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity ','cart_counter': get_cart_counter(request), 'qty':checkcart.quantity ,'cart_amount': get_cart_amounts(request) })
                except:
                    checkcart =Cart.objects.create(user=request.user, fooditem = fooditem , quantity =1)
                    return JsonResponse({'status': 'Success', 'message': ' Add the food to the cart' ,'cart_counter': get_cart_counter(request), 'qty':checkcart.quantity ,'cart_amount': get_cart_amounts(request) })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'The food does not exit'})
            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Plesase login to  continue'})
    

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            #Check if the food item exit

            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    checkcart =Cart.objects.get(user=request.user, fooditem = fooditem )
                    if checkcart.quantity > 1:

                    #Decrease  the cart quantity
                        checkcart.quantity -= 1
                        checkcart.save()
                    else:
                        checkcart.delete()
                        checkcart.quantity = 0
                    return JsonResponse({'status': 'Success','cart_counter': get_cart_counter(request), 'qty':checkcart.quantity, 'cart_amount': get_cart_amounts(request) })
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart '  })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'The food does not exit'})
            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Plesase login to  continue'})
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #Check if the item exit
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Succcess', 'message': 'Cart Item deleted successfully!','cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exit'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        

def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    # get the vendor ids that has the fooditem the user is looking for
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword,is_approved=True, user__is_active=True))

    vendor_count = vendors.count()
    context = {
        'vendors':   vendors,
        'vendor_count': vendor_count
    }

    return render(request, 'marketplace/listings.html',context)