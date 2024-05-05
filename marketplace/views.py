from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .context_processors import get_cart_counter

from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch

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
                    return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity ','cart_counter': get_cart_counter(request), 'qty':checkcart.quantity })
                except:
                    checkcart =Cart.objects.create(user=request.user, fooditem = fooditem , quantity =1)
                    return JsonResponse({'status': 'Success', 'message': ' Add the food to the cart' ,'cart_counter': get_cart_counter(request), 'qty':checkcart.quantity  })
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
                    return JsonResponse({'status': 'Success','cart_counter': get_cart_counter(request), 'qty':checkcart.quantity })
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart '  })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'The food does not exit'})
            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Plesase login to  continue'})
    
    