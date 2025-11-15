"""ACRepairingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from random import randint
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_login/', admin_login, name="admin_login"),
    path('user_login/', user_login, name="user_login"),
    path('technician_login/', technician_login, name="technician_login"),
    path('logout_technician/', logout_technician, name="logout_technician"),
    path('request_form/', request_form, name="request_form"),
    path('user_register/', user_register, name="user_register"),
    path('reg_user/', reg_user, name="reg_user"),
    path('user_profile/', user_profile, name="user_profile"),
    path('technician_profile/', technician_profile, name="technician_profile"),
    path('change_password/', change_password, name="change_password"),
    path('admin_change_password/', admin_change_password, name="admin_change_password"),
    path('technician_change_password/', technician_change_password, name="technician_change_password"),
    path('logout_admin/', logout_admin, name="logout_admin"),
    path('logout_user/', logout_user, name="logout_user"),
    path('dashboard/', dashboard, name="dashboard"),
    path('user_dashboard/', user_dashboard, name="user_dashboard"),
    path('technician_dashboard/', technician_dashboard, name="technician_dashboard"),
    path('requestlist/', requestlist, name="requestlist"),
    path('request_detail/<int:pid>/', request_detail, name="request_detail"),
    path('request_detail1/<int:pid>/', request_detail1, name="request_detail1"),
    path('user_cancel_request/<int:pid>/', user_cancel_request, name="user_cancel_request"),
    path('add_brand/', add_brand, name="add_brand"),
    path('add_technician/', add_technician, name="add_technician"),
    path('manage_brand/', manage_brand, name="manage_brand"),
    path('manage_technician/', manage_technician, name="manage_technician"),
    path('edit_brand/<int:pid>/', edit_brand, name="edit_brand"),
    path('edit_technician/<int:pid>/', edit_technician, name="edit_technician"),
    path('change_profile_image/<int:pid>/', change_profile_image, name="change_profile_image"),
    path('delete_brand/<int:pid>/', delete_brand, name="delete_brand"),
    path('delete_technician/<int:pid>/', delete_technician, name="delete_technician"),
    path('edit_about/', edit_about, name="edit_about"),
    path('edit_contact/', edit_contact, name="edit_contact"),
    path('delete_request/<int:pid>/', delete_request, name="delete_request"),
    path('between_dates_report/', between_dates_report, name="between_dates_report"),
    path('employee_wise_report/', employee_wise_report, name="employee_wise_report"),
    path('sales_report/', sale_report, name="sales_report"),
    path('technician_report/', technician_report, name="technician_report"),
    path('admin_search_request/', admin_search_request, name="admin_search_request"),
    path('technician_search_request/', technician_search_request, name="technician_search_request"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
