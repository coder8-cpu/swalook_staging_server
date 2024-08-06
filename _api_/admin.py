from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(VendorService)
admin.site.register(VendorPdf)
admin.site.register(VendorAppointment)
admin.site.register(VendorInvoice)
admin.site.register(VendorStaff)
admin.site.register(SwalookUserProfile)
admin.site.register(SalonBranch)