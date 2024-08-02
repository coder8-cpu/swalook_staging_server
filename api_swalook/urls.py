"""api_swalook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from _api_.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('update_file/', update_files_pull.as_view()),
    path("restart_server/", restart_server.as_view()),
    # path('swalook_token_ii091/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('swalook_token_ii091/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
    path('api/swalook/endpoints/',showendpoint.as_view()),
    path('api/swalook/create_account/',VendorSignin.as_view()),
    path('api/swalook/centralized/login/',Centralized_login.as_view()),
    path('api/swalook/login/',vendor_login.as_view()),
    path('api/swalook/staff/login/',staff_login.as_view()),
    path('api/swalook/admin/login/',admin_login.as_view()),
  
    path('api/swalook/billing/',vendor_billing.as_view()),
    path('api/swalook/save-pdf/',vendor_billing_pdf.as_view()),
    path('api/swalook/appointment/',VendorAppointments.as_view()),
    path('api/swalook/appointment/<branch_name>/',VendorAppointments.as_view()),
    path('api/swalook/edit/appointment/<id>/',edit_appointment.as_view()),
    path('api/swalook/delete/appointment/<id>/',delete_appointment.as_view()),
    path('api/swalook/delete/invoice/<id>/',Delete_invoice.as_view()),
    path('api/swalook/edit/profile/<id>/',edit_profile.as_view()),
    path('api/swalook/preset-day-appointment/',present_day_appointment.as_view()),
    path('api/swalook/services/',VendorServices.as_view()),
    path('api/swalook/add/services/',Add_vendor_service.as_view()),
    path('api/swalook/table/services/',Table_service.as_view()),
    path('api/swalook/edit/services/<id>/',Edit_service.as_view()),
    path('api/swalook/delete/services/<id>/',Delete_service.as_view()),
    path('api/swalook/get_specific/appointment/<id>/',get_specific_appointment.as_view()),
    path('api/swalook/get_specific_slno/',get_slno.as_view()),
    path('api/swalook/get_current_user/<id>/',get_current_user_profile.as_view()),
 
    path('api/swalook/get_present_day_bill/',get_present_day_bill.as_view()),
    path('api/swalook/get_bill_data/<id>/',get__bill.as_view()),
    path('api/swalook/get_branch_data/<branch_name>/<date>/',render_branch_data.as_view()),
    
    path('api/swalook/help_desk/',help_desk.as_view()),

    path('api/swalook/salonbranch/',VendorBranch.as_view()),
    path('api/swalook/edit/salonbranch/<id>/',edit_branch.as_view()),
    path('api/swalook/delete/salonbranch/<id>/',delete_branch.as_view()),
    path('api/swalook/verify/<salon_name>/<branch_name>/',user_verify.as_view()),
    path('api/swalook/send/otp/<email>/',ForgotPassword.as_view()),
    path('api/swalook/verify/<otp>/',ForgotPassword.as_view()),
    path('api/swalook/analysis/month/business/_01/',BusniessAnalysiss.as_view()),
    path('api/swalook/inventory/product/add/',Add_Inventory_Product.as_view()),
    path('api/swalook/inventory/product/edit/<id>/',Add_Inventory_Product.as_view()),
    path('api/swalook/inventory/product/delete/<id>/',Add_Inventory_Product.as_view()),
    path('api/swalook/inventory/product/show/<branch_name>/',Add_Inventory_Product.as_view()),
    path('api/swalook/inventory/invoice/',Bill_Inventory.as_view()),
    path('api/swalook/loyality_program/add/customer/<branch_name>/',Vendor_loyality_customer_profile.as_view()),

    
    
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
