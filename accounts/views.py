from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator


# from accounts.utils import detectUser, send_verification_email
from vendor.forms import VendorForm
# from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode


   
def registerUser(request):
    # if request.user.is_authenticated:
    #     messages.warning(request,'You are already login')
        # return redirect('registerUser')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # created the user using form for hashing password
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER 
            # user.save()
            
            # created the user using create_user method in model
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save() 
            
            #Send verification Email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/acc_verify_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your account have been register successfully')
            return redirect('registerUser')
        
        #checking error field in form
        else:       
            print('Invalit Form')
            print(form.errors)
            
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)



def registerVendor(request):
    # if request.user.is_authenticated:
    #     messages.warning(request,'You are already login')
    #     return redirect('vendorDashboard')
    if request.method =='POST':
        #Store the data and Create User
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile= user_profile
            vendor.save()
    
            # #Send verification Email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/acc_verify_email.html'
            # send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your account have been register successfully Please wait for approval.')
            return redirect('registerVendor')
        else:
            print('Invalit Form')
            print(form.errors)
                    
                
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context)