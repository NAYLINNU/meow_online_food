from django.urls import path, include
from . import views
from accounts import views as Accountviews

urlpatterns = [
    
    path('',Accountviews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name='v_profile'),
    # path('menu-builder/',views.menu_builder, name='menu_builder')
    



]
