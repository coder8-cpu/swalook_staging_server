from django.contrib.auth.models import User
from django.core import validators
from django.db import models
import datetime as dt
import uuid

class SalonBranch(models.Model):
    
    id                  = models.UUIDField   (default=uuid.uuid4,primary_key=True,  editable=False)
    vendor_name         = models.ForeignKey  (User,               on_delete=models.CASCADE, null=True)
    
    
    staff_name          = models.CharField   (max_length=1000,)
  
    
    branch_name         = models.CharField   (max_length=1000,)
   
    password            = models.CharField   (max_length=11,      null=True ,blank=True)
    admin_password            = models.CharField   (max_length=11,      null=True ,blank=True)
   
    staff_url      = models.CharField   (max_length=1000,)
    admin_url      = models.CharField   (max_length=1000,)
    

    class Meta:
        ordering = ['vendor_name']
        verbose_name = "Vendor Branch"
    def __str__(self) -> str:
        return str(self.vendor_name)


class SwalookUserProfile(models.Model):  
    id                    = models.UUIDField    (    default=uuid.uuid4,primary_key=True,editable=False)
    salon_name            = models.CharField    (    max_length=1000)
    owner_name            = models.CharField    (    max_length=1000)
    profile_pic           = models.ImageField   (    blank=True,null=True)
    mobile_no             = models.CharField    (    max_length=10,)
    email                 = models.EmailField   (    null=True,blank=True,)
    vendor_id             = models.CharField    (    null=False,max_length=6) 
    invoice_limit         = models.IntegerField (    default=0,null=True,editable=True) 
    account_created_date  = models.DateField(    auto_now_add=False,null=True    )
    user_ip               = models.CharField    (    max_length=200,    null=True,         blank=True)
    gst_number            = models.CharField    (    max_length=20,     null=True,         blank=True) 
    pan_number            = models.CharField    (    max_length=20,     null=True,         blank=True) 
    pincode               = models.CharField    (    max_length=20,     null=True,         blank=True) 
    number_of_staff       = models.IntegerField (    default=0)
    s_gst_percent         = models.CharField    (    max_length=30)
    c_gst_percent         = models.CharField    (    max_length=30)
    current_billslno      = models.CharField    (    max_length=50)
    appointment_limit     = models.IntegerField (    default=0,       null=True,   editable=True)
    invoice_generated     = models.IntegerField ()
    appointment_generated = models.IntegerField ()
    enc_pwd               = models.CharField    (    max_length=1000)
    branch_limit          = models.IntegerField (    default=1,null=True,editable=True) 
    branches_created          = models.IntegerField (    default=0,null=True,editable=True) 
    class Meta:
        ordering = ['salon_name']
        verbose_name = "Vendor_Profile"
        unique_together = [["salon_name","mobile_no"]]

    def __str__(self):
        return str(self.salon_name)

class Vendor_Service(models.Model): 
    id             = models.UUIDField (default=uuid.uuid4,primary_key=True,  editable=False)
    user           = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    service        = models.CharField(max_length=30)

    service_price  = models.CharField(max_length=30)
    
    service_duration  = models.CharField(max_length=30)
    vendor_branch = models.ForeignKey(SalonBranch,on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ['service']
        verbose_name = "Vendor_Service"
        # unique_together = [["name","mobile_no"]]


    def __str__(self):
        return str(self.service)



class VendorInvoice(models.Model):
    id                 = models.UUIDField    (    default=uuid.uuid4,primary_key=True,  editable=False)
    slno               = models.CharField    (max_length=50,     null=True,      blank=True)

    customer_name      = models.CharField    (max_length=1000,)
    address            = models.CharField    (max_length=200,null=True,         blank=True)
    mobile_no          = models.CharField    (max_length=10,null=True,               blank=True)
    email              = models.CharField    (max_length=50,null=True,                      blank=True)
    services           = models.CharField    (max_length=100000,)
    service_by         = models.CharField    (max_length=40,)
    total_prise        = models.DecimalField (default=0,    max_digits=100,       decimal_places=2,  null=True,  blank=True)
    total_tax          = models.DecimalField (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_discount     = models.DecimalField (null=True,      blank=True,     decimal_places=2, max_digits=100,default=0)
    gst_number         = models.CharField    (max_length=20,  blank=True,     null=True) # device limit
   
    total_quantity     = models.IntegerField (default=0)
    total_cgst         = models.DecimalField (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_sgst         = models.DecimalField (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    grand_total        = models.DecimalField (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    vendor_name        = models.ForeignKey   (User,on_delete=models.SET_NULL,null=True)
    date               = models.DateField    ()
    month              = models.CharField    (max_length=30,null=True,blank=True)
    week               = models.CharField    (max_length=30,null=True,blank=True)
    year               = models.CharField    (max_length=30,null=True,blank=True)
    vendor_branch = models.ForeignKey(SalonBranch,on_delete=models.SET_NULL,null=True)
    vendor_branch_name =  models.CharField    (max_length=100000,)
    comment =  models.CharField    (max_length=100000,null=True,blank=True)
   
    class Meta:
        ordering = ['date']
        verbose_name = "Vendor Invoice"

    def __str__(self):
        return str(self.vendor_name)
class VendorPdf(models.Model):
    id                 = models.UUIDField    (    default=uuid.uuid4,primary_key=True,  editable=False)
    vendor_branch = models.ForeignKey(SalonBranch,on_delete=models.SET_NULL,null=True)
    invoice = models.CharField(max_length=100000000)
    mobile_no = models.CharField(max_length=1000000)
    email = models.CharField(max_length=1000)
    customer_name = models.CharField(max_length=1000)
    file = models.FileField   (upload_to="pdf",blank=True,null=True)
    vendor_branch_name =  models.CharField    (max_length=100000,)
    
    date =  models.DateField()
    
    class Meta:
        ordering = ['date']
        verbose_name = "Vendor Invoice Pdf"

    def __str__(self):
        return str(self.vendor_branch)
    
class VendorAppointment(models.Model):  # model objects for store appointments
    id             = models.UUIDField   (default=uuid.uuid4,primary_key=True,  editable=False)
    vendor_name    = models.ForeignKey  (User,               on_delete=models.CASCADE, null=True)
    customer_name  = models.CharField   (max_length=100,     null=True, blank=True)
    mobile_no      = models.CharField   (max_length=10,        null=True, blank=True)
    email          = models.CharField   (max_length=100,         null=True, blank=True)
    services       = models.CharField   (max_length=100000,          null=True, blank=True)
    
    booking_date   = models.CharField   (max_length=100,                  null=True, blank=True)
    booking_time   = models.CharField   (max_length=100,                  null=True, blank=True)

   
    # status_completed = models.BooleanField(null=True, blank=True)
    # status_canceled = models.BooleanField(null=True, blank=True)
    date            = models.DateField()
    vendor_branch = models.ForeignKey(SalonBranch,on_delete=models.SET_NULL,null=True)
    comment =  models.CharField    (max_length=100000,null=True,blank=True)
    file_pdf = models.FileField   (upload_to="pdf",blank=True,null=True)
    class Meta:
        ordering = ['date']
        verbose_name = "Vendor Appointment"

    def __str__(self):
        return str(self.vendor_name)

class VendorStaff(models.Model):
    id                  = models.UUIDField   (default=uuid.uuid4,primary_key=True,  editable=False)
    vendor_name         = models.ForeignKey  (User,               on_delete=models.CASCADE, null=True)
    staff_name          = models.CharField   (max_length=1000,)
    mobile_no           = models.CharField   (max_length=13,      null=True ,blank=True)
    is_user_staff       = models.BooleanField()
    password            = models.CharField   (max_length=11,      null=True ,blank=True)
    billing_permission  = models.BooleanField()
    appointment_permission  = models.BooleanField()
    vendor_branch = models.ForeignKey(SalonBranch,on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['vendor_name']
        verbose_name = "Vendor Staff"
    def __str__(self) -> str:
        return str(self.staff_name)



class BusinessAnalysis(models.Model):
    id                  = models.UUIDField   (default=uuid.uuid4,primary_key=True,  editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    monthly_analysis = models.ImageField(upload_to="analysis",null=True)
    month = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return str(self.user)


class HelpDesk(models.Model):
    id                  = models.UUIDField   (default=uuid.uuid4,primary_key=True,  editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    mobile_no = models.CharField(max_length=1000)
    message = models.CharField(max_length=10000000)
    def __str__(self) -> str:
        return str(self.user)













