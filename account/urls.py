from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),        # customer login
    path('logout/', views.customer_logout, name='customer_logout'),

    path('admin/login/', views.admin_login, name='admin_login'),        # admin login
    path('admin/logout/', views.admin_logout, name='admin_logout'),

    path('home/', views.home, name='home'),
]
