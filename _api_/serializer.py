from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import serializers
from .models import *
from rest_framework.response import Response
import datetime as dt
import random as r 
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password,check_password
import requests
from api_swalook.settings import WP_INS_TOKEN,WP_INS_ID,WP_API_URL
from api_swalook.settings import BASE_DIR
from api_swalook import settings
import pdfkit as p
import http.client
class signup_serializer(ModelSerializer):
    class Meta:
        model = SwalookUserProfile
        fields = ["salon_name","mobile_no","email","owner_name"]
    def create(self, validated_data):
        # signup_obj.vendor_id      = name_[0:2] + str(a) + str(b) + str(c)
        #         get_ip                    = request.META.get('HTTP_X_FORWARDED_FOR') # ip
        #         if get_ip:
        #             self.ip               = get_ip.split(',')[0]
        #         else:
        #             self.ip               = request.META.get('REMOTE_ADDR')
        #         signup_obj.ip             = self.ip
        #         signup_obj.dev_limit      = 1
        #         signup_obj.gst_number     = 0
        #         signup_obj.s_gst_percent  = "0"
        #         signup_obj.c_gst_percent  = "0"
        #         signup_obj.save()
        a = r.randint(0,9)
        b = r.randint(0,9)
        c = r.randint(0,9)
        validated_data['vendor_id'] = validated_data["salon_name"][0:2] + str(int(a)) + str(int(b)) + str(int(c))
        validated_data['invoice_limit'] = 100
        validated_data['account_created_date'] = dt.date.today()
        get_ip                    = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR') # ip
        if get_ip:
            ip               = get_ip.split(',')[0]
        else:
            ip               = self.context.get('request').META.get('REMOTE_ADDR')
        validated_data['user_ip'] = str(ip)
        validated_data['number_of_staff'] = "0"
        validated_data['s_gst_percent'] = "0"
        validated_data['c_gst_percent'] = "0"
        validated_data['current_billslno'] = "0"
        validated_data['appointment_limit'] = 100
        validated_data['invoice_generated'] = 0
        validated_data['appointment_generated'] = 0
        validated_data['gst_number'] = "0"
        validated_data['pan_number'] = "0"
        validated_data['pincode'] = "0"
        validated_data['profile_pic'] = "/data/inv.png/"
        validated_data['enc_pwd'] = "w!==?0id"
        user = User()
        user.username = validated_data['mobile_no']
        user.set_password("w!==?0id")
        user.save()
        return super().create(validated_data)
        
class login_serializer(serializers.Serializer):

    mobileno = serializers.CharField()
    password = serializers.CharField()

  
    def create(self, validated_data):
       
        user = auth.authenticate(username=validated_data['mobileno'],password=validated_data['password'])
        if user is not None:
           auth.login(self.context.get('request'),user)
       


        return "ok!"
        
        

class centralized_login_serializer(serializers.Serializer):

    mobileno = serializers.CharField()
    password = serializers.CharField()

    
    def create(self, validated_data):
       
        user = auth.authenticate(username=validated_data['mobileno'],password=validated_data['password'])
        if user is not None:
           auth.login(self.context.get('request'),user)
           token = Token.objects.get_or_create(user=user)
           
           return ["owner",token]
       
        else:
            
            staff_object = SalonBranch.objects.filter(staff_name=validated_data['mobileno'],password=validated_data.get('password'))
            if len(staff_object) == 1:
                u = SwalookUserProfile.objects.filter(mobile_no=staff_object[0].vendor_name)
                if len(u) == 1:
                    user = auth.authenticate(username=u[0].mobile_no,password=u[0].enc_pwd)
                    auth.login(self.context.get('request'),user)
                    token = Token.objects.get_or_create(user=user)
                    return ["staff",token]
                else:
                    return "error-509"
                    
            else:
                u = User.objects.filter(username=validated_data['mobileno'])
                if len(u) == 1:
                    admin_obj = SalonBranch.objects.filter(vendor_name=u[0],admin_password=validated_data.get('password'))
                    if len(admin_obj) == 1:
                        u = SwalookUserProfile.objects.filter(mobile_no=validated_data['mobileno'])
                        user = auth.authenticate(username=u[0].mobile_no,password=u[0].enc_pwd)
                        auth.login(self.context.get('request'),user)
                        token = Token.objects.get_or_create(user=user)
                        return ["admin",token]
                    else:
                         return "error-508"
                else:
                    
                    return "error-507"
            return "main-510"
        

        
class admin_login_serializer(serializers.Serializer):

    mobileno = serializers.CharField()
    password = serializers.CharField()

  
    def create(self, validated_data):
     
        u = SwalookUserProfile.objects.get(mobile_no=validated_data.get('mobileno'))
  
        branch = SalonBranch.objects.get(admin_password=validated_data.get('password'))
        user = auth.authenticate(username=u.mobile_no,password=u.enc_pwd)
        auth.login(self.context.get('request'),user)
        token = Token.objects.get_or_create(user=user)
            
                
   
        
            
        # u = User.objects. # user = auth.authenticate(username=u.username,password=u.password)
            
        # if user is not None:
        #     auth.login(self.context.get('request'),user)
                # get(pk=user_sub.ve)
            
       


        return token
        
        
class staff_login_serializer(serializers.Serializer):

    mobileno = serializers.CharField()
    password = serializers.CharField()

  
    def create(self, validated_data):
       
        user_sub = SalonBranch.objects.get(staff_name=validated_data['mobileno'],password=validated_data['password'])
        # if len(user_sub) == 1:
        #     main_user = SwalookUserProfile.objects.get(id=user_sub[0].vendor_name_id)
            
            
        #     user = auth.authenticate(username=main_user.mobile_no,password=main_user.enc_pwd)
            
        #     if user is not None:
        #         auth.login(self.context.get('request'),user)

        return user_sub.vendor_name
    

class update_profile_serializer(serializers.Serializer):

    gst_number = serializers.CharField()
    profile_pic = serializers.ImageField()
    s_gst_percent = serializers.CharField()
    c_gst_percent = serializers.CharField()
  
    def update(self, validated_data):
       object = SwalookUserProfile.objects.get(mobile_no=str(self.context.get('request').user))
       object.profile_pic = self.context.get('request').FILES.get('profile_pic')
       object.gst_number = validated_data['gst_number']
       object.s_gst_percent = validated_data['s_gst_percent']
       object.c_gst_percent = validated_data['c_gst_percent']
       object.save()
       return super().update(validated_data)
    
        
    
class billing_serailizer(serializers.ModelSerializer):
    class Meta:
        model = VendorInvoice
        fields = ["customer_name","mobile_no","email","address","services","service_by","total_prise","total_quantity","total_tax","total_discount","grand_total","total_cgst","total_sgst","gst_number","vendor_branch_name","comment","slno"]

    def create(self,validated_data):
        date = dt.date.today()
        mon = dt.date.today()
        m_ = mon.month
        y_ = mon.year
      
        if int(mon.day) >=1 and int(mon.day) <=7:

            validated_data['week'] = "1"
        if int(mon.day) >=8 and int(mon.day) <=15:
            validated_data['week'] = "2"
        if int(mon.day) >=16 and int(mon.day) <=23:
            validated_data['week']= "3"
        if int(mon.day) >=24 and int(mon.day) <=31:
            validated_data['week']= "4"
        
      
        
     
        validated_data['vendor_name'] = self.context.get('request').user
        validated_data['date'] = date
        validated_data['month'] = mon.month
        validated_data['vendor_branch'] =  SalonBranch.objects.get(branch_name=validated_data['vendor_branch_name'])
       
        validated_data['year'] = mon.year
        
        super().create(validated_data)
       
        
      
       
           

        return  validated_data['slno']
    
class billing_serailizer_get(serializers.ModelSerializer):
    class Meta:
        model = VendorInvoice
        fields = "__all__"
        
class app_serailizer_get(serializers.ModelSerializer):
    class Meta:
        model = VendorAppointment
        fields = "__all__"
        

class appointment_serializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAppointment
 
        fields = ["id","customer_name","mobile_no","email","services","booking_date","booking_time","comment","file_pdf"]
        extra_kwargs = {'id':{'read_only':True},}
    def create(self,validated_data):
        validated_data['vendor_name'] = self.context.get('request').user
        validated_data['vendor_branch'] = SalonBranch.objects.get(branch_name=self.context.get('branch_name'))
        
        validated_data['date'] = dt.date.today()
        validated_data['file_pdf'] = self.context.get('request').FILES.get('file_pdf')
        super().create(validated_data)
        if validated_data['email'] != " ":
            subject = "Swalook - Appointment"
            body = f"Hi {validated_data['customer_name']}!\nYour appointment is booked and finalised for:{validated_data['booking_time']} | {validated_data['booking_date']}\nFor the following services: {validated_data['services']}\nSee you soon!\nThanks and Regards\nTeam {self.context.get('branch_name')}"
            send_mail(subject,body,'info@swalook.in',[validated_data['email']])
            
        # if validated_data['mobile_no'] != None:

        #     url = f"{WP_API_URL}"
            
        #     payload = f"token={WP_INS_TOKEN}&to=+91{validated_data['mobile_no']}&body=Hi {validated_data['customer_name']}! Your appointment is booked and finalised for:{validated_data['booking_time']} |{validated_data['booking_date']} For the following services: {validated_data['services']} See you soon! Thanks & Regards Team {self.context.get('branch_name')}"
        #     payload = payload.encode('utf8').decode('iso-8859-1')
        #     headers = {'content-type': 'application/x-www-form-urlencoded'}
            
        #     response = requests.request("POST", url, data=payload, headers=headers)

        return "ok"
    
class update_appointment_serializer(serializers.Serializer):
    customer_name  = serializers.CharField()
    mobile_no      = serializers.CharField()
    email          = serializers.EmailField()
    services       = serializers.CharField()
    booking_date   = serializers.CharField()
    booking_time   = serializers.CharField()
    # status_pending = serializers.BooleanField()
    # status_completed = serializers.BooleanField()
    # status_cancelled = serializers.BooleanField()
    # date           = serializers.DateField()


class Vendor_Pdf_Serializer(serializers.ModelSerializer):
        
    class Meta:
        model = VendorPdf
        fields = ["customer_name","mobile_no","file","vendor_branch_name","email","invoice"]
        extra_kwargs = {'id':{'read_only':True},}
        
    def create(self,validated_data):
        vendor_branch_name = SalonBranch.objects.get(branch_name=validated_data['vendor_branch_name'])
        validated_data['vendor_branch'] = vendor_branch_name
        
      
        validated_data['date'] = dt.date.today()
        validated_data['file'] = self.context.get('request').FILES.get('file')
        
        return super().create(validated_data)
        
        
        
    

    



    
class service_serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Service
        fields = ["id","service","service_price","service_duration","vendor_branch"]
        extra_kwargs = {'id':{'read_only':True},}
    def create(self,validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    
class service_update_serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Service
        fields = ["service","service_price","service_duration",]
    def create(self,validated_data):
        queryset = Vendor_Service.objects.get(id=self.context.get('id'))
        
        queryset.delete()
        queryset = Vendor_Service()


        queryset.service = validated_data.get("service")
        queryset.service_duration = validated_data.get('service_duration')
        queryset.service_price = validated_data.get('service_price')
        queryset.user = self.context.get('request').user
        queryset.save()

        return super().create(validated_data)
    


class service_name_serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Service
        fields = ["id","service",]

class staff_serializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStaff
        fields = ["staff_name","billing_permission","is_user_staff","mobile_no","password","appointment_permission","vendor_branch"]

class user_data_set_serializer(serializers.ModelSerializer):
    class Meta:
        model = SwalookUserProfile
        fields = "__all__"
        
        
class staff_serializer_get(serializers.ModelSerializer):
    class Meta:
        model = VendorStaff
        fields = "__all__"

class branch_serializer(serializers.ModelSerializer):
    class Meta:
        model = SalonBranch
        fields = ["id","staff_name","branch_name","password","admin_password","staff_url","admin_url"]
        extra_kwargs = {'id':{'read_only':True},}
        
    def create(self,validated_data):
        validated_data['vendor_name'] = self.context.get('request').user
        validated_data['admin_password'] = str(self.context.get('request').user)[:3]+str(validated_data['branch_name'])[:3]
        validated_data['staff_url'] =  validated_data['branch_name']+"/staff/" 
        validated_data['admin_url'] = validated_data['branch_name']+"/admin/" 
        validated_data['password'] = validated_data['password']
        validated_data['branch_name'] = validated_data['branch_name'] 
        validated_data['staff_name'] = validated_data['staff_name']
     
        return super().create(validated_data)
    
class HelpDesk_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HelpDesk
        fields = ["id","first_name","last_name","mobile_no","email","message",]
        extra_kwargs = {'id':{'read_only':True},}
        
    def create(self,validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    
       
