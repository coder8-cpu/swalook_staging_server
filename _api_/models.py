from django.contrib.auth.models import User
from django.core import validators
from django.db import models
import datetime as dt
import uuid


class SalonBranch(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    staff_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    password = models.CharField(max_length=11, blank=True)
    admin_password = models.CharField(max_length=11, blank=True)
    staff_url = models.CharField(max_length=255)
    admin_url = models.CharField(max_length=255)

    class Meta:
        ordering = ['vendor_name']
        verbose_name = "Vendor Branch"

    def __str__(self) -> str:
        return str(self.vendor_name)


class SwalookUserProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    salon_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(blank=True, null=True)
    mobile_no = models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    vendor_id = models.CharField(max_length=6)
    invoice_limit = models.IntegerField(default=0, null=True)
    account_created_date = models.DateField(null=True)
    user_ip = models.CharField(max_length=200, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    number_of_staff = models.IntegerField(default=0)
    s_gst_percent = models.CharField(max_length=30)
    c_gst_percent = models.CharField(max_length=30)
    current_billslno = models.CharField(max_length=50)
    appointment_limit = models.IntegerField(default=0, null=True)
    invoice_generated = models.IntegerField()
    appointment_generated = models.IntegerField()
    enc_pwd = models.CharField(max_length=1000)
    branch_limit = models.IntegerField(default=1, null=True)
    branches_created = models.IntegerField(default=0, null=True)
    minimum_purchase_loyality = models.IntegerField(default=100, null=True)

    class Meta:
        ordering = ['salon_name']
        verbose_name = "Vendor Profile"
        unique_together = [["salon_name", "mobile_no"]]

    def __str__(self):
        return str(self.salon_name)


class VendorLoyalityProgramTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=255)
    program_type = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self) -> str:
        return str(self.user)


class VendorCustomers(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=30)
    vendor_branch_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30)
    membership_type = models.CharField(max_length=30)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Vendor Customers"


class VendorCustomerLoyalityPoints(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_name = models.ForeignKey(VendorCustomers, on_delete=models.SET_NULL, null=True)
    current_customer_points = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    issue_date = models.DateField()
    expire_date = models.DateField()
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['customer_name']
        verbose_name = "Vendor Customers Points"


class VendorService(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    service = models.CharField(max_length=30)
    service_price = models.CharField(max_length=30)
    service_duration = models.CharField(max_length=30)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['service']
        verbose_name = "Vendor Service"

    def __str__(self):
        return str(self.service)


class VendorInvoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    slno = models.CharField(max_length=50, blank=True)
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=200, blank=True)
    mobile_no = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=50, blank=True)
    services = models.CharField(max_length=10000)
    service_by = models.CharField(max_length=40)
    total_prise = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True)
    total_tax = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True)
    total_discount = models.DecimalField(max_digits=100, decimal_places=2, default=0, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    total_quantity = models.IntegerField(default=0)
    total_cgst = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True)
    total_sgst = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True)
    grand_total = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True)
    vendor_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    month = models.CharField(max_length=30, blank=True)
    week = models.CharField(max_length=30, blank=True)
    year = models.CharField(max_length=30, blank=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_customers_profile = models.ForeignKey(VendorCustomers, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)
    loyalty_points = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['date']
        verbose_name = "Vendor Invoice"

    def __str__(self):
        return str(self.vendor_name)


class VendorPdf(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    invoice = models.CharField(max_length=1000)
    mobile_no = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="pdf", blank=True, null=True)
    vendor_branch_name = models.CharField(max_length=255)
    date = models.DateField()
    vendor_email = models.CharField(max_length=255)
    vendor_password = models.CharField(max_length=255)

    class Meta:
        ordering = ['date']
        verbose_name = "Vendor Invoice Pdf"

    def __str__(self):
        return str(self.vendor_branch)


class VendorAppointment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=255, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    services = models.CharField(max_length=255)

    booking_date = models.DateField()
    date = models.DateField()
    booking_time = models.TimeField()
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['booking_date']
        verbose_name = "Vendor Appointment"

    def __str__(self):
        return str(self.vendor_name)

class VendorStaff(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    staff_name = models.CharField(max_length=1000)
    mobile_no = models.CharField(max_length=13, null=True, blank=True)
    is_user_staff = models.BooleanField()
    password = models.CharField(max_length=11, null=True, blank=True)
    billing_permission = models.BooleanField()
    appointment_permission = models.BooleanField()
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['vendor_name']
        verbose_name = "Vendor Staff"

    def __str__(self) -> str:
        return str(self.staff_name)


class BusinessAnalysis(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    monthly_analysis = models.ImageField(upload_to="analysis", null=True, blank=True)
    month = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return str(self.user)


class HelpDesk(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    mobile_no = models.CharField(max_length=1000)
    message = models.TextField() 

    def __str__(self) -> str:
        return str(self.user)


class VendorInventoryProduct(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_id = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=1000)
    product_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    product_description = models.TextField() 
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=1000)
    stocks_in_hand = models.IntegerField(default=0)
    date = models.DateField()
    month = models.CharField(max_length=30, null=True, blank=True)
    week = models.CharField(max_length=30, null=True, blank=True)
    year = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.product_name)


class VendorInventoryInvoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(VendorCustomers, on_delete=models.SET_NULL, null=True)
    mobile_no = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=1000)
    product = models.ForeignKey(VendorInventoryProduct, on_delete=models.SET_NULL, null=True)
    product_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()
    loyalty_points = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    total_quantity = models.IntegerField(default=0)
    total_cgst = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_sgst = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField()
    month = models.CharField(max_length=30, null=True, blank=True)
    week = models.CharField(max_length=30, null=True, blank=True)
    year = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.product)


class VendorCustomerLoyalityLedger(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=1000)
    customer = models.ForeignKey(VendorCustomerLoyalityPoints, on_delete=models.SET_NULL, null=True)
    point_spend = models.IntegerField()
    point_available = models.IntegerField()
    invoice_obj = models.ForeignKey(VendorInvoice, on_delete=models.CASCADE, null=True)
    inventory_invoice_obj = models.ForeignKey(VendorInventoryInvoice, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    month = models.CharField(max_length=30, null=True, blank=True)
    week = models.CharField(max_length=30, null=True, blank=True)
    year = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)


class VendorLoyalitySettings(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor_branch = models.ForeignKey(SalonBranch, on_delete=models.SET_NULL, null=True)
    vendor_branch_name = models.CharField(max_length=1000)
    program_type = models.ForeignKey(VendorLoyalityProgramTypes, on_delete=models.SET_NULL, null=True)
    duration = models.IntegerField()
    points_hold = models.IntegerField()

    def __str__(self) -> str:
        return str(self.user)