from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
import io
from api_swalook import urls
import requests
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
import datetime as dt
from django.shortcuts import render
from .analysis import *
from .models import *
import random as r
import matplotlib.pyplot as plt
import pandas as pd
from api_swalook.settings import WP_INS_TOKEN,WP_INS_ID,WP_API_URL
import os
import matplotlib
from api_swalook.settings import BASE_DIR
import magic

from django.core.mail import EmailMessage
class VendorSignin(CreateAPIView):

   
    permission_classes = [AllowAny] 
    serializer_class = signup_serializer
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = signup_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = signup_serializer(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
            
           
            return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'user':serializer.validated_data.get('salon_name'),
                'mobileno':serializer.validated_data.get('mobile_no'),
                "text" :  "User_created",

            },)
        return Response({
            'status':False,
             "text": "serializer data is invalid !"
        },)



class vendor_update_profile(APIView):
    permission_classes = [IsAuthenticated]
    def update(self,request):
        serializer_objects           = update_profile_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = update_profile_serializer(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()   
        return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'code':302,
                "text" : "User_data_updated",

            },)


class vendor_login(CreateAPIView):

    serializer_class = login_serializer
    permission_classes = [AllowAny]
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = login_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = login_serializer(data=accept_json_stream,context={"request":request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
            user = User.objects.get(username=request.user)
            token = Token.objects.get_or_create(user=user)
            salon_name = SwalookUserProfile.objects.get(mobile_no=str(request.user))
            if salon_name.branches_created != 0:
                branch = SalonBranch.objects.get(vendor_name=user)
                return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'code': 302,
                'text' : "login successfull !",
                'token': str(token[0]),
                'user': str(request.user),
                'salon_name':salon_name.salon_name,
                'type':"vendor",
                
                'branch_name':branch.branch_name,
                })
            else:
                
            
            
           
                return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code': 302,
                    'text' : "login successfull !",
                    'token': str(token[0]),
                    'user': str(request.user),
                    'salon_name':salon_name.salon_name,
                    'type':"vendor",
                    
                  
        
        
                },)
        return Response({
            'status':False,
            'code':500,
            'text':'invalid user&pass'
            
        },)

class staff_login(CreateAPIView):

    serializer_class = staff_login_serializer
    permission_classes = [AllowAny]
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = staff_login_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = staff_login_serializer(data=accept_json_stream,context={"request":request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            u=serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
            use = SwalookUserProfile.objects.get(mobile_no=str(u.username))
            user = auth.authenticate(username=use.mobile_no,password=use.enc_pwd)
            auth.login(request,user)
            # user = User.objects.get(username=request.user)
            token = Token.objects.get_or_create(user=user)
            salon_name = SwalookUserProfile.objects.get(mobile_no=str(request.user))
            user = User.objects.get(username=salon_name.mobile_no)
            branch = SalonBranch.objects.get(vendor_name=user)
            
            


            
           
            return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'code': 302,
                'text' : "login successfull !",
                'token': str(token[0]),
                'user': str(request.user),
                'salon_name':salon_name.salon_name,
                'type':"staff",
                
                'branch_name':branch.branch_name,
                

            },)
        return Response({
            'status':False,
            'code':500,
            'text':'invalid user&pass'
            
        },)

class admin_login(CreateAPIView):

    serializer_class = admin_login_serializer
    permission_classes = [AllowAny]
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = admin_login_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = admin_login_serializer(data=accept_json_stream,context={"request":request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            token = serializer.save()  
            # user = auth.authenticate(username=u.username,password=u.password)
            # the create method of serializer call here 
            ''' returning the status and info as response'''
           
            
            
            salon_name = SwalookUserProfile.objects.get(mobile_no=str(request.user))
            user = User.objects.get(username=salon_name.mobile_no)
            branch = SalonBranch.objects.get(vendor_name=user)
            


            
           
            return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'code': 302,
                'text' : "login successfull !",
                'token': str(token[0]),
                'user': str(request.user),
                'salon_name':salon_name.salon_name,
                'type':"admin",
                'branch_name':branch.branch_name,

            },)
        return Response({
            'status':False,
            'code':500,
            'text':'invalid user&pass'
            
        },)
        

class Centralized_login(CreateAPIView):
    serializer_class = centralized_login_serializer
    permission_classes = [AllowAny]
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = centralized_login_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = centralized_login_serializer(data=accept_json_stream,context={"request":request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            token = serializer.save()  
            # user = auth.authenticate(username=u.username,password=u.password)
            # the create method of serializer call here 
            ''' returning the status and info as response'''
           
            
            
            salon_name = SwalookUserProfile.objects.get(mobile_no=str(request.user))
            user = User.objects.get(username=salon_name.mobile_no)
          
            if salon_name.branches_created != 0:
                    branch = SalonBranch.objects.get(vendor_name=user)
            
            
           
                    return Response({
                        'status':True,                                                      # corresponding to ---> 'key:value' for access data
                        'code': 302,
                        'text' : "login successfull !",
                        'token': str(token[1][0]),
                        'user': str(request.user),
                        'salon_name':salon_name.salon_name,
                        'type':f"{token[0]}",
                        'branch_name':branch.branch_name,
        
                    },)
            else:
                return Response({
                        'status':True,                                                      # corresponding to ---> 'key:value' for access data
                        'code': 302,
                        'text' : "login successfull !",
                        'token': str(token[1][0]),
                        'user': str(request.user),
                        'salon_name':salon_name.salon_name,
                        'type':f"{token[0]}",
                        
        
                    },)
        return Response({
            'status':False,
            'code':500,
            'text':'invalid user&pass'
            
        },)


class VendorServices(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        queryset = Vendor_Service.objects.filter(user=request.user).order_by('service')
        serialized_data = service_name_serializer(queryset,many=True)
        
        return Response({
                'status':True,                                                      # corresponding to ---> 'key:value' for access data
                'code':302,
                'service':serialized_data.data
                

            },)
    
class Add_vendor_service(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = service_serializer
    def post(self,request):
        serializer_objects           = service_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = service_serializer(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()       

            return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code':302,
                    'text':"service added !"

                    

                },)


class Edit_service(CreateAPIView):    
    permission_classes = [IsAuthenticated]
    serializer_class = service_update_serializer
    def post(self,request,id):
        serializer_objects           = self.serializer_class(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = self.serializer_class(data=accept_json_stream,context={'request':request,"id":id})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()       

            return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code':302,
                    'text':"service updated !"

                    

                },)


    
    
class Delete_service(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        queryset = Vendor_Service.objects.get(id=id)
        queryset.delete()

        return Response({
                'status':True,                                                   
                'service_deleted_id':id,
                

            },)
            

            
class Delete_invoice(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        queryset = VendorInvoice.objects.get(id=id)
        queryset.delete()

        return Response({
                'status':True,                                                   
                'invoice_deleted_id':id,
                

            },)
            


class Table_service(APIView):
 
    def get(self,request):
        query_set = Vendor_Service.objects.filter(user=request.user).order_by('service')
        serializer_obj = service_serializer(query_set,many=True)
        return Response({
            "status":True,
            "table_data":serializer_obj.data,

        })
class get_slno(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
  
        mon = dt.date.today()
        m_ = mon.month
        y_ = mon.year
        v_id = SwalookUserProfile.objects.get(mobile_no=str(request.user))
        v_id.invoice_generated = int(int(v_id.invoice_generated)+1)
        v_id.save()
        slno = v_id.vendor_id.lower() + str(v_id.invoice_generated) + str(m_) + str(y_) + str(v_id.invoice_generated)
       
            
        
       
        
        
       
        return Response({
            "slno":slno,    
        })
    
class vendor_billing(CreateAPIView,ListAPIView,):
    permission_classes = [IsAuthenticated]
    serializer_class = billing_serailizer
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = billing_serailizer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = billing_serailizer(data=accept_json_stream,context={'request':request})               # intializing serializer and
        
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            slnoo = serializer.save()  
            # the create method of serializer call here 
            ''' returning the status and info as response'''
            # inv =  VendorInvoice.objects.get(slno=slnoo)
           
         
            return Response({
                "status":True,
                "slno":slnoo,
                
                
            
         
            
            

            })
        return Response({
                "status":False,
               
            
         
            
            

        })
    
    def list(self,request):
      
        query_set = VendorInvoice.objects.filter(vendor_name=request.user)[::-1]
        query_set_salon_name = SwalookUserProfile.objects.get(mobile_no=str(request.user))
        serializer_obj = billing_serailizer_get(query_set,many=True)
        return Response({
            "status":True,
            "table_data":serializer_obj.data,
            "salon_name":query_set_salon_name.salon_name,

        })

class vendor_billing_pdf(CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer_objects           = Vendor_Pdf_Serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
        
        serializer                   = Vendor_Pdf_Serializer(data=accept_json_stream,context={"request":request})               
        # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()   
            
            # if serializer.data.get('mobile_no') != " ":
            #     url = f"https://api.ultramsg.com/{WP_INS_ID}/messages/chat"
                
            #     payload = f"token={WP_INS_TOKEN}&to=+91{request.data.get('mobile_no')}&body=Hi {request.data.get('customer_name')}!\nWe hope you had a pleasant experience at {request.data.get('vendor_branch_name')}.\nWe are looking forward to servicing you again, attached is the invoice.\nThanks and Regards \nTeam {request.data.get('vendor_branch_name')}"
            #     payload = payload.encode('utf8').decode('iso-8859-1')
            #     headers = {'content-type': 'application/x-www-form-urlencoded'}
                
            #     response = requests.request("POST", url, data=payload, headers=headers)
                
                
                # url = f"https://api.ultramsg.com/{WP_INS_ID}/messages/document"
                
             
    
    
                
                # payload = f"token={WP_INS_TOKEN}&to=+91{request.data.get('mobile_no')}&filename=Invoice.pdf&document={serializer.data.get('file')}"
                # payload = payload.encode('utf8').decode('iso-8859-1')
                # headers = {'content-type': 'application/x-www-form-urlencoded'}
    
                # response = requests.request("POST", url, data=payload, headers=headers)
            
            if serializer.data.get('email') != " ":
                if "gmail" in serializer.data.get('email'):
                    settings.EMAIL_BACKEND = 'smtp.gmail.com'
                else:

                    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                settings.EMAIL_HOST = serializer.data.get('vendor_branch_name') # e.g., mail.yourdomain.com
                settings.EMAIL_PORT = 465 # Update the port accordingly (587 for TLS, 465 for SSL, 25 for non-secure)
                settings.EMAIL_USE_TLS = False  # Set to False if using SSL
                settings.EMAIL_USE_SSL =  True  # Set to True if using SSL
                settings.EMAIL_HOST_USER = serializer.data.get('vendor_email') # Your email username
                settings.EMAIL_HOST_PASSWORD = serializer.data.get('vendor_password') # Your email password
                settings.DEFAULT_FROM_EMAIL = serializer.data.get('vendor_email')    # The default "from" address for sending emails

                # subject = "Swalook - Invoice"
                # body = f"Hi {request.data.get('customer_name')}!\nWe hope you had a pleasant experience at {request.data.get('vendor_branch_name')}.\nWe are looking forward to servicing you again, attached is the invoice.\nThanks and Regards \nTeam {request.data.get('vendor_branch_name')}"
                # send_mail(subject,body,'deshabandhumahavidyalaya@dbmcrj.ac.in',[request.data.get('email')])
                with open(f"{BASE_DIR}/media/pdf/Invoice-{serializer.data.get('invoice')}.pdf", 'rb') as file:

                    subject = f"{serializer.data.get('vendor_branch_name')} - Invoice"
                    body = f"Hi {request.data.get('customer_name')}!\nWe hope you had a pleasant experience at {request.data.get('vendor_branch_name')}.\nWe are looking forward to servicing you again, attached is the invoice.\nThanks and Regards \nTeam {request.data.get('vendor_branch_name')}"
                    from_email = serializer.data.get('vendor_email')
                    recipient_list = [request.data.get('email')]
                    file_content = file.read()
            
                    mime_type = magic.from_buffer(file_content, mime=True)
            
                    # Extract the filename from the attachment_path
                    # file_name = os.path.basename(serializer.data.get('file'))
            
                    email = EmailMessage(subject, body, from_email, recipient_list)
                    email.attach(f"Invoice-{serializer.data.get('invoice')}.pdf", file_content, mime_type)
            
                # Send the email
                    email.send()
                    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                    settings.EMAIL_HOST = 'mail.swalook.in' # e.g., mail.yourdomain.com
                    settings.EMAIL_PORT = 465 # Update the port accordingly (587 for TLS, 465 for SSL, 25 for non-secure)
                    settings.EMAIL_USE_TLS = False  # Set to False if using SSL
                    settings.EMAIL_USE_SSL =  True  # Set to True if using SSL
                    settings.EMAIL_HOST_USER = 'info@swalook.in'  # Your email username
                    settings.EMAIL_HOST_PASSWORD = 'rf4TwJbh456#' # Your email password
                    settings.DEFAULT_FROM_EMAIL = 'info@swalook.in'  # The default "from" address for sending emails      

            return Response({
                "status":True,
            

        })
        return Response({
                "status":False,
            

        })
            

class VendorAppointments(CreateAPIView,ListAPIView,):
    permission_classes = [IsAuthenticated]
    serializer_class = appointment_serializer
    def post(self,request,branch_name):
        ''' deserialization of register user'''
        serializer_objects           = appointment_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = appointment_serializer(data=accept_json_stream,context={"request":request,"branch_name":branch_name})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
  
            if request.data.get('mobile_no') != " ":
                url = f"https://api.ultramsg.com/{WP_INS_ID}/messages/chat"
                
                payload = f"token={WP_INS_TOKEN}&to=+91{request.data.get('mobile_no')}&body=Hi {request.data.get('customer_name')}!\nYour appointment is booked and finalised for:{request.data.get('booking_time')} | {request.data.get('booking_date')}\nFor the following services: {request.data.get('services')}\nSee you soon!\nThanks and Regards\nTeam {branch_name}"
                payload = payload.encode('utf8').decode('iso-8859-1')
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                
                response = requests.request("POST", url, data=payload, headers=headers)
                
                return Response({
                    "status":True,
                    "msg":"wp msg sent",
                
    
                })
                
            return Response({
                    "status":True,
                
    
                })
                
        return Response({
            "status":False,
            

            })
    
    def list(self,request):
        query_set = VendorAppointment.objects.filter(vendor_name=request.user)[::-1]
        serializer_obj = appointment_serializer(query_set,many=True)
        return Response({
            "status":True,
            "table_data":serializer_obj.data,

        })
   

class edit_appointment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
         
        accept_json_stream           =  request.data       

        queryset = VendorAppointment.objects.get(id=id)
        
        queryset.delete()
        queryset = VendorAppointment()
        queryset.customer_name =     accept_json_stream.get('customer_name')
        queryset.mobile_no     =     accept_json_stream.get('mobile_no')
        queryset.email         =     accept_json_stream.get('email')
        queryset.services      =     accept_json_stream.get('services')
        queryset.booking_time  =     accept_json_stream.get('booking_time')
        queryset.booking_date  =     accept_json_stream.get('booking_date')
        # queryset.status_pending    = accept_json_stream.get('status_pending')
        # queryset.status_completed =  accept_json_stream.get('status_completed')
        # queryset.status_canceled  =  accept_json_stream.get('status_cancelled')
        queryset.date =  dt.date.today()
        queryset.vendor_name = request.user
        vendor_branchs = SalonBranch.objects.get(branch_name=request.data.get('vendor_branch'),vendor_name=request.user)
        queryset.vendor_branch = vendor_branchs
        queryset.comment = accept_json_stream.get('comment')
        queryset.save()  

        return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code':302,
                    'text':"appointment update!"

                

        },)
        
        
class edit_profile(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
         
        accept_json_stream           =  request.data       

        queryset = SwalookUserProfile.objects.get(mobile_no=id)
        

      
        
        queryset.owner_name    =     accept_json_stream.get('owner_name')
  
        queryset.email      =     accept_json_stream.get('email')
        queryset.gst_number  =     accept_json_stream.get('gst_number')
        queryset.pan_number  =     accept_json_stream.get('pan_number')
        queryset.pincode  =     accept_json_stream.get('pincode')
        # queryset.status_pending    = accept_json_stream.get('status_pending')
        # queryset.status_completed =  accept_json_stream.get('status_completed')
        # queryset.status_canceled  =  accept_json_stream.get('status_cancelled')
        
        queryset.save()  

        return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code':302,
                    'text':"user profile updated!"

                

        },)
        
        
    

class delete_appointment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        queryset = VendorAppointment.objects.get(id=id)
        
        queryset.delete()
        return Response({
            "status":True,
            'code':302,
            "appointment_deleted_id":id,
          
        })
class VendorBranch(CreateAPIView,RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = branch_serializer
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = branch_serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = self.serializer_class(data=accept_json_stream,context={"request":request})  
  
        accept_json_stream           =  request.data       
        test_if = SalonBranch.objects.filter(staff_name=accept_json_stream.get('staff_name'))
        if len(test_if) == 1:
            return Response({"status":"this mobileno is already registered with a licence !",})
        user_if = SalonBranch.objects.filter(staff_name=accept_json_stream.get('staff_name'),vendor_name=request.user)
        if len(user_if) == 1:
            return Response({"status":"this mobileno is already registered on this licence !",})
        branch_if  =  SalonBranch.objects.filter(branch_name=accept_json_stream.get('branch_name'),staff_name=accept_json_stream.get('staff_name'),vendor_name=request.user)
        if len(branch_if) == 1:
            return Response({"status":"this branch with this username is already exists !",})
        only_branch_if  =  SalonBranch.objects.filter(branch_name=accept_json_stream.get('branch_name'),vendor_name=request.user)
        if len(only_branch_if) == 1:
            return Response({"status":"this branch is already exists on this licence !",})
        user_profile = SwalookUserProfile.objects.get(mobile_no=str(request.user))
        if user_profile.branch_limit == user_profile.branches_created:
            return Response({
                "status":"this licence is reached its branch limit !",})
        
        # try:
        #     staff_object = VendorStaff.objects.get(mobile_no=accept_json_stream.get('staff_name'))
        # except Exception as e:
        #     return Response({
        #         "status":f"this number {accept_json_stream.get('staff_name')} is not associated with any staff mobile no",})
        queryset = SalonBranch()
        

    
        queryset.branch_name =     accept_json_stream.get('branch_name')
        queryset.staff_name     =     accept_json_stream.get('staff_name')
        queryset.password         =     accept_json_stream.get('password')
        queryset.admin_password      =     accept_json_stream.get('branch_name')[:5]+str(request.user)[:7]
        queryset.staff_url  =  accept_json_stream.get('branch_name')
        queryset.admin_url  =  accept_json_stream.get('branch_name')
        queryset.vendor_name  =  request.user
        queryset.save()
        
        user_profile.branches_created = user_profile.branches_created + 1
        user_profile.save()
        
        
        ''' returning the status and info as response'''
        return Response({
            "status":True,
            "admin_password":queryset.admin_password,
            

        })
  
    
    def get(self,request):
        query_set = SalonBranch.objects.filter(vendor_name=request.user)[::-1]
        serializer_obj = branch_serializer(query_set,many=True)
        return Response({
            "status":True,
            "table_data":serializer_obj.data,

        })
   

class edit_branch(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
         
        accept_json_stream           =  request.data       

        queryset = SalonBranch.objects.get(id=id)
        
        queryset.delete()
        queryset = SalonBranch()
          
        queryset.branch_name    =     accept_json_stream.get('branch_name')
        queryset.staff_name         =     accept_json_stream.get('staff_name')
        queryset.password     =     accept_json_stream.get('password')
        queryset.admin_password  =     accept_json_stream.get('admin_password')
        queryset.staff_url =     accept_json_stream.get('staff_url')
        queryset.admin_url =     accept_json_stream.get('admin_url')
        # queryset.status_pending    = accept_json_stream.get('status_pending')
        # queryset.status_completed =  accept_json_stream.get('status_completed')
        # queryset.status_canceled  =  accept_json_stream.get('status_cancelled')
       
        queryset.vendor_name = request.user
        queryset.save()  

        return Response({
                    'status':True,                                                      # corresponding to ---> 'key:value' for access data
                    'code':302,
                    'text':"branch update!"

                

        },)
        
        
    

class delete_branch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        queryset = SalonBranch.objects.get(id=id)
        
        queryset.delete()
        user_profile = SwalookUserProfile.objects.get(mobile_no=str(request.user))
        user_profile.branches_created = user_profile.branches_created - 1
        user_profile.save()
        return Response({
            "status":True,
            'code':302,
            "branch_deleted_id":id,
          
        })
        

class user_verify(APIView):
    permission_classes = [AllowAny]
    def get(self,request,salon_name,branch_name):
        try:
            sallon_name = SwalookUserProfile.objects.filter(salon_name=salon_name)
            user = User.objects.get(username=sallon_name[0].mobile_no)
            queryset = SalonBranch.objects.get(vendor_name=user,branch_name=branch_name,)
            
            
            return Response({
                "status":True,
                'code':302,
                
              
            })
        except Exception as e:
            return Response({
                "status":False,
                'code':302,
                
              
            })
            

class present_day_appointment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        date = dt.date.today()
        query_set = VendorAppointment.objects.filter(vendor_name=request.user,date=date).order_by("booking_time")
        serializer_obj = appointment_serializer(query_set,many=True)
        return Response({

            "status":True,
            "table_data":serializer_obj.data,
        })
    
class get_specific_appointment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        date = dt.date.today()
        query_set = VendorAppointment.objects.filter(id=id)
        serializer_obj = appointment_serializer(query_set,many=True)
        return Response({

            "status":True,
            "single_appointment_data":serializer_obj.data,
        })
    

    


class showendpoint(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({
            "status":True,

            "endpoints": ""
            
        })


import subprocess

class update_files_pull(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
      
        command = ['git','pull']
        
        try:
           
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during command execution
            output = f"Error: {e.stderr}"
        return Response({
            "server updated" : output,
        })
    
class restart_server(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
      
        os.chdir("/root/api_swalook/Swalook-master/")
        command = ['npm','run','build']
        command2 = ['PORT=80','serve','-s','build']
        

        
        try:
     
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout
            result_ = subprocess.run(command, capture_output=True, text=True, check=True)
            output_ = result_.stdout
            return Response({
            "server build status" : output,
            "server running" : output_,
            "status": True,
            })
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during command execution
            output = f"Error: {e.stderr}"
            return Response({
            "error":output,
            "status": False,
            })

class get_current_user_profile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        data = SwalookUserProfile.objects.get(mobile_no=id)
        serializer_data = user_data_set_serializer(data)
        return Response({
            "status":True,
            "current_user_data":serializer_data.data,

        })

class get_present_day_bill(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        data = VendorInvoice.objects.filter(date=dt.date.today())
        serializer_data = billing_serailizer_get(data,many=True)
        return Response({
            "status":True,
            "current_user_data":serializer_data.data,

        })

class get__bill(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self,request,id):
        data = VendorInvoice.objects.filter(id=id)
        serializer_data = billing_serailizer_get(data,many=True)
        return Response({
            "status":True,
            "current_user_data":serializer_data.data,

        })
        
        
class render_branch_data(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,branch_name,date):
        # try:
            salon_branch = SalonBranch.objects.get(vendor_name=request.user,branch_name=branch_name)
            main_user = SwalookUserProfile.objects.get(mobile_no=str(request.user))
            # staff = VendorStaff.objects.get(vendor_name=request.user,vendor_branch=salon_branch.branch_name,mobile_no=salon_branch[0].staff_name,)
            inv = VendorInvoice.objects.filter(vendor_name=request.user,vendor_branch=salon_branch,date=date)
            app = VendorAppointment.objects.filter(vendor_name=request.user,vendor_branch=salon_branch,date=str(date))
            # stf = VendorStaff.objects.filter(vendor_name=request.user,vendor_branch=salon_branch,date=date)
            # ser = VendorService.objects.filter(vendor_name=request.user,vendor_branch=salon_branch,date=date)
            
            serializer_data_bill = billing_serailizer_get(inv,many=True)
            serializer_data_appo = appointment_serializer(app,many=True)

            
            
            return Response({
                "status":True,
                "branch_name":salon_branch.branch_name,
                "salon_name":main_user.salon_name,
                
                "invoices": serializer_data_bill.data,
                "appointment": serializer_data_appo.data
                # "services":serializer_data_serv,
                # "staff":serializer_data_staf,
                
 # except Exception as e:
        #     return Response({
        #     "status":"this branch is deleted by the vendor",
            

        # })
        })
       
class ForgotPassword(APIView):
    permission_classes = [AllowAny]
    def __init__(self):
        self.otp = None
    
    def get(self,request,email):
        import random as r
        a = r.randint(0,9)
        b = r.randint(0,9)
        c = r.randint(0,9)
        d = r.randint(0,9)
        e = r.randint(0,9)
        f = r.randint(0,9)
        request.session['otp_990'] = f"{a}{b}{c}{d}{e}{f}"
        
        # try:
        user = SwalookUserProfile.objects.get(email=email)
        subject = "Swalook - OTP Verification"
        body = f"your 6 digit otp is {request.session.get('otp_990')}. \n Thank you\n Swalook"
        send_mail(subject,body,'info@swalook.in',[user.email])
        # except Exception:
        #     return Response({
        #     "status":"invalid email-id",
        # })
        
        return Response({
            "status":True,
        })
    def post(self,request,otp):
        
        if otp == request.session.get("otp_990"):
            return Response({
                "status":True,
                
            })
        else:
            return Response({
                "status":False,
                "message":"Invalid OTP",
                
                
            })
    
class BusniessAnalysiss(APIView):
    permission_classes = [IsAuthenticated]
    def __init__(self):
        self.mon = dt.date.today()
       
       

    
    def get(self,request,):
        def monthly_analysis(self,data={}):

            matplotlib.use('agg')
            data = data# converting response into json format
         
            x_values = []

            y_values = [0]
            for item in data['data']:
                    if item['date'] in x_values:
                            pass
                    else:
                            x_values.append(item['date']) #giving x field
            i = 0
            value = 0
            for item in data['data']:
                    if x_values[i] == item['date']:

                            value = value + float(item['grand_total'])
                    else:
                            print(value)
                            y_values.append(int(value)) #giving y field
                            i = i+1
                            value = 0
            z_value = []
            for i in x_values:
                    txt = i[6:10]
                    txt = txt + " "
                    z_value.append(txt)
                    x_values = z_value
            # giving chart x and y axis labels
            # plt.bar(x_values,y_values, color =['green'])
            # plt.xlabel("Date")
            # plt.ylabel("Total Billing amount")
            # saving plot
            # path = os.path.join(BASE_DIR/'media/analysis', "analysis")
          
            # plt.savefig(path+f'monthly_analysis_01.webp')
            # return f'https://api.crm.swalook.in/media/analysis/analysismonthly_analysis_01.webp'
            return y_values
        self.month = self.mon.month
        # b = BusinessAnalysis.objects.filter(user=request.user,month=self.month)
        # if b.exists():
        #     b.delete()

        # a = Analysis(user="abc")
        queryset = VendorInvoice.objects.filter(vendor_name=request.user,month=self.month)
        serializer = billing_serailizer_get(queryset,many=True)
        path = monthly_analysis(self,data={"data":serializer.data})
        
        # b = BusinessAnalysis()
        # b.user = request.user
        # b.monthly_analysis = f"{path}"
        # b.month= self.month
        # b.save()
        return Response({
                "status":True,
                "data":path
                
                
            })
            
class help_desk(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HelpDesk_Serializer
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = HelpDesk_Serializer(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = HelpDesk_Serializer(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
            subject = "Swalook - Query form "
            body = f" {serializer.data}. \n Thank you\n Swalook"
            send_mail(subject,body,'info@swalook.in',["info@swalook.in"])
            return Response({
            "status":True,
            'from mail':'info@swalook.in',
            'to mail':'info@swalook.in',
            })
            
            
        
    
    

    
class Add_Inventory_Product(CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Inventory_Product_Serializer
    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = self.serializer_class(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = self.serializer_class(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
           
            return Response({
            "status":True,
            "data":serializer.data

            
            

        })
    
    
    def put(self,request,id):
        pass
    def delete(self,request,id):
        data_object = VendorInventoryProduct.objects.get(user=request.user,id=id)
        data_object.delete()
        return Response({
            "status":True,
           
        })


    def list(self,request,branch_name):
        data_object = VendorInventoryProduct.objects.filter(user=request.user,vendor_branch_name=branch_name)[::-1]
        serializer_obj  = self.serializer_class(data_object,many=True)

        return Response({
            "status":True,
            "data":serializer_obj.data
        })
    


class Bill_Inventory(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Inventory_Product_Invoice_Serializer

    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = self.serializer_class(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = self.serializer_class(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
           
            return Response({
            "status":True,
            "data":serializer.data
            })
    

class Vendor_loyality_customer_profile(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorCustomerLoyalityProfileSerializer

    def post(self,request):
        ''' deserialization of register user'''
        serializer_objects           = self.serializer_class(request.data)                 # convertion of request.data into python native datatype
        json_data                    = JSONRenderer().render(serializer_objects.data)      # rendering the data into json
        stream_data_over_network     = io.BytesIO(json_data)                                 # streaming the data into bytes
        accept_json_stream           = JSONParser().parse(stream_data_over_network)            # prases json data types data
        ''' passing the json stream data into serializer '''
    
        serializer                   = self.serializer_class(data=accept_json_stream,context={'request':request})               # intializing serializer and
        if serializer.is_valid():                                                                   # check if serializer.data is valid 
                                                                                    # all the .validate_fieldname in the serializer will call here
            ''' here the db call happen after accept  '''
            
            serializer.save()                                                       # the create method of serializer call here 
            ''' returning the status and info as response'''
           
            return Response({
            "status":True,
            "data":serializer.data
            })
    


    


    

