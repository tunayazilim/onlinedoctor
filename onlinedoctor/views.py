from datetime import date, datetime
from functools import reduce
import json
import locale
import math
from multiprocessing import context
from pickle import NONE
from telnetlib import EL
from time import time
from unittest import result
from django.contrib.sites.models import Site
from django.db.models import Q
from django.db.models.functions.datetime import ExtractYear
from django.utils import tree
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import (get_object_or_404, redirect, render,
                              )
from django.urls import reverse
from django.views.generic.base import TemplateView
from pytz import timezone
from Admin.models import PageModel
from chat.models import Message, Room, peerInformations
from config.settings.base import RECAPTCHA_PRIVATE_KEY
import iyzipay
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from onlinedoctor.forms import (CommentModelForm, DoctorBasicForm,
                                PatientBasicForm, TimeScheduleModelForm, iletisimSettingsModelForm, iletişimModelForm, registerForm,
                                socialMediaDoctorForm)

from .models import (ClinicImages, CommentModel, CustomUserModel, FavouriteModel, TimeScheduleModel, alanModel,
                     alanYazilarModel, appointmentModel, awardsDoctorModel, bannerModel, deletedAppointmentModel, doctorFeatureIndexModel,
                     educationDoctorModel, experienceDoctorModel, featureModel, footerModel, iletisimSettingsModel, indexDoktorlarYaziModel, logoModel,
                     socialMediaDoctorModel)
            
from onlinedoctor.templatetags.load_active_day import load_active_day_of
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime
from datetime import timedelta
import requests
import calendar
UserModel = get_user_model()


# Create your views here.


def user_is_doctor_check(user):
    return user.is_doctor



def user_is_patient_check(user):
    return user.is_patient



def index(request):
    # for i in CustomUserModel.objects.all():
    #     i.save()
    #Room.objects.get(id="715600ccc54746acb0bdedf2ec26a674").delete()
    # for us in TimeScheduleModel.objects.all():
    #     us.delete()
        
    # for i in appointmentModel.objects.all():
    #     i.delete()

    # for i in deletedAppointmentModel.objects.all():
    #     i.delete()

    # for i in Room.objects.all():
    #     i.delete()
    
    # for i in Message.objects.all():
    #     i.delete()

    # for i in iletisimSettingsModel.objects.all():
    #     i.delete()
        
    #CommentModel.objects.all().delete()
    # for date in TimeScheduleModel.objects.filter(doctor=request.user).all():
    #     date.delete()
    # appointmentModel.objects.all().delete()
    #TimeScheduleModel.objects.all().delete()
   # CustomUserModel.objects.exclude(email="mm@gmail.com").delete()
    # Room.objects.filter(first_user_id=5).all().delete()
    #Message.objects.all().delete()     
    # not_doctors=Room.objects.all().exclude(first_user_id=3)
    # for i in not_doctors:
    #     i.delete()
    #sec=CustomUserModel.objects.get(email="muhammetay651@gmail.com")
   # fis=CustomUserModel.objects.get(email="hh@gmail.com")
   # CustomUserModel.objects.get(email="muhammed.aydogan@ceng.deu.edu.tr").delete()
 #   CustomUserModel.objects.get(username="muhammet19071340@gmail.com").delete()
   # CustomUserModel.objects.get(username="muhammet").delete()
   #thi=CustomUserModel.objects.get(email="muhammed.aydogan@ceng.deu.edu.tr")
  #  Room.objects.create(first_user=sec,second_user=fis)
    #Room.objects.create(first_user=sec,second_user=thi)
    banner=bannerModel.objects.all().first()
    alanyazi=alanYazilarModel.objects.all().first()
    alanlar=alanModel.objects.all()
    allFeatures=featureModel.objects.all()
    featureDoctor=doctorFeatureIndexModel.objects.first()
    meta_data=PageModel.objects.filter(view_name="index").first()
    aciklamaYazisi=indexDoktorlarYaziModel.objects.first()
    favorite_list=[]
    if request.user.is_authenticated:
        favourites=FavouriteModel.objects.filter(patient=request.user)
        for favourite in favourites:
            favorite_list.append(favourite.doctor.pk)
    context = {
        "banner":banner,
        "alanyazi":alanyazi,
        "alanlar":alanlar,
        "allFeatures":allFeatures,
        "featureDoctor":featureDoctor,
        "doctors":CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True),
        "favorite_list":favorite_list,
        "meta_data":meta_data,
        "aciklamaYazisi":aciklamaYazisi,
        "whichPageforCity":"indexPage"
        
    }
    return render(request,"index.html",context)


def recaptcha_check(recaptcha_response): #2
    verify_url = 'https://www.google.com/recaptcha/api/siteverify' #3
    value = { #4
        'secret': RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    response = requests.post(verify_url, value) #5
    result = response.json() #6
    if result['success'] is True: #7
        return True
    else: #8
        return {'status': result['success'], 'reason': result['error-codes']} #


def register_doctor(request):
    type="Doktor"
    if request.method == "GET":
        # us=get_object_or_404(CustomUserModel,email="muhammed.aydogan@ceng.deu.edu.tr")
        # us.delete()
        form = registerForm()
        return render(request, "register.html",{"form":form,"type":type})
    if request.method == "POST":
        form = registerForm(request.POST or None,request.FILES or None)
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        if recaptcha_response_result is not True:
            messages.error(request,"Lütfen robot olmadığınızı kanıtlamak için captcha güzevnlik kontrolümüzü onaylayınız.")
            return render(request, "register.html",{"form":form,"type":type})
        if recaptcha_response_result is True and form.is_valid():
            data=form.save(commit=False)
            if request.FILES['kimlik'].size > 10485760 or request.FILES['file'].size > 10485760:
                messages.error(request,"Yüklediğiniz dosya boyutu en fazla 10 mb olmalıdır.")
                return render(request, "register.html",{"form":form,"type":type})
            data.is_doctor=True
            data.username= form.cleaned_data.get("email")
            data.is_active = False   
            data.none_average_star=5
            data.save()
            current_site = request.META['HTTP_HOST']    
            mail_subject = 'Hesabını aktif et'
            message = render_to_string('acc_active_email.html', {
                'user': data,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(data.pk)),
                'token': default_token_generator.make_token(data),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "email_not.html",{"note":"Mail adresinizden linke tıklayarak kaydınızı tamamlayınız","class_name":"fas fa-envelope"})
            # username = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password1")
            # user = authenticate(username=username,password=password)
            # login(request,user)
            # return redirect("index")
        else:
            messages.error(request,form.errors,extra_tags="registerDoctorError")
            return render(request, "register.html",{"form":form,"type":type})
    else:
        form = registerForm()
    context = {
        "form":form,
        "type":type

    }
    return render(request, "register.html",context)



def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if user.is_patient == True:
            user.is_active = True
            user.save()
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("index")
        else:
            user.save()
     #   user = authenticate(username=user.username,password=user.)
       # login(request,user)
            return render(request, "email_not.html",{"note":"Teşekkür Ederiz.Yöneticimiz kaydınızı gözden geçirip onayladığında mail adresinize mail gelecek ve ardından servisimizi kullanmaya başlayabilirsiniz","class_name":"fas fa-envelope"})
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def register_patient(request):
    type="Hasta"
    # if request.method == "GET":
    #     us=get_object_or_404(CustomUserModel,email="muhammetay651@gmail.com")
    #     us.delete()
    #     form = registerForm()
    #     return render(request, "register.html",{"form":form,"type":type})
    if request.method == "POST":

        #send_mail( 'Subject here', 'Here is the message.', 'muhammetay651@gmail.com', ['muhammetay651@gmail.com'],)
        form = registerForm(request.POST or None)
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        if recaptcha_response_result is not True:
            messages.error(request,"Lütfen robot olmadığınızı kanıtlamak için captcha güzevnlik kontrolümüzü onaylayınız.")
            return render(request, "register.html",{"form":form,"type":type})
        if recaptcha_response_result is True and form.is_valid():
            data=form.save(commit=False)
          #  data.image="avatar/no-avatar.png"
            data.is_patient=True
            data.username= form.cleaned_data.get("email")
            data.is_active = False
            data.save()
            current_site = request.META['HTTP_HOST']   
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': data,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(data.pk)),
                'token': default_token_generator.make_token(data),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "email_not.html",{"note":"Mail adresinizden linke tıklayarak kaydınızı tamamlayınız","class_name":"fas fa-envelope"})
            # username = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password1")
            # user = authenticate(username=username,password=password)
            # login(request,user)
            # return redirect("index")
        else:
            messages.error(request,form.errors,extra_tags="registerPatientError")        
            return render(request, "register.html",{"form":form,"type":type,})
    else:
        form = registerForm()
    context = {
        "form":form,
        "type":type

    }
    return render(request, "register.html",context)





def loginindex(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)		
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)             
                user.online="onsite"
                user.is_active_now=False
                user.save()
                return redirect("index")
            else:
                messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
        else:
            messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})




def logoutindex(request):
    user=get_object_or_404(CustomUserModel,email=request.user.email)
    user.online="offline"
    user.is_active_now=True
    user.save()
    logout(request)
    return redirect("login")
    



# @permission_required('is_doctor',login_url="login")
@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def showDoctorProfileSettings(request):
    #print (request.POST)

    # for key, value in request.POST.items():
    #     print('Key: %s' % (key) ) 
    #     print('Value %s' % (value) )
  
    if request.user.is_doctor:
        context = {
            "clinic_images":ClinicImages.objects.filter(user=request.user),
            "educations":educationDoctorModel.objects.filter(user=request.user),
            "experiences":experienceDoctorModel.objects.filter(user=request.user),
            "awards":awardsDoctorModel.objects.filter(user=request.user),
            "which_active":"profile",
            "whichPageforCity":"settingsPage",
            
        }
        if request.method == "POST":
            user=get_object_or_404(CustomUserModel,pk=request.user.pk)
            user.first_name=request.POST["first_name"]
            user.last_name=request.POST["last_name"]
            user.phone_number=request.POST["phone_number"]
            user.gender=request.POST["gender"]
            user.date_of_birth=request.POST["date_of_birth"]
            user.about=request.POST.get("about"," ")
            user.define_profession=request.POST.get("define_profession"," ")
            user.clinic_name=request.POST.get("clinic_name"," ")
            user.unvan=request.POST.get("unvan"," ")
            user.clinic_address=request.POST.get("clinic_address"," ")
            user.country=request.POST.get("country"," ")
            user.city=request.POST.get("city"," ")
            user.cityCode=request.POST.get("cityCode"," ")
            user.state=request.POST.get("state"," ")
            user.address=request.POST.get("address"," ")
            user.services=request.POST.get("services"," ")
            user.specializations=request.POST.get("specialist"," ")
            # if 'degree' not in request.POST:
            #     pass
            # else:
            #     print(request.POST.getlist('degree')[1]+" degree ksımları bundan sonra sonra var mı")
            #     for name in request.POST.getlist('degree'):
            #         print(name)
            if request.POST["rating_option"] == "price_free":
                user.is_free=True
                user.custom_price=0
            elif request.POST["rating_option"] == "custom_price":
                user.is_free=False
                try:
                    val = int(request.POST["appointment_minute"])
                except ValueError:
                    val = 0
                try:
                    cus = int(request.POST["custom_rating_count"])
                except ValueError:
                    cus = 0
               # minutes=request.POST.get("appointment_minute","0")
                user.appointment_minute=val
                user.custom_price=cus
            if 'imageavatar' not in request.FILES:
                pass
            else:
                user.image=request.FILES["imageavatar"] #FILES
            if ('degree' in request.POST.keys() and request.POST['degree']) or ('college' in request.POST.keys() and request.POST['college']) or ('year_of_completion' in request.POST.keys() and request.POST['year_of_completion']):
                # print("değerler geliyor")
                # list=[]
                # cc=len(request.POST.getlist('degree'))
                # list.append(len(request.POST.getlist('degree')))
                # list.append(len(request.POST.getlist('college')))
                # list.append(len(request.POST.getlist('year_of_completion')))
                # list.sort()
                user.educationsofdoctor.all().delete()
                for x in range(len(request.POST.getlist('degree'))):  #normalde list[-1] yazıyordu max değeri almak için
                    deg=request.POST.getlist('degree')[x]
                    col=request.POST.getlist('college')[x]
                    year=request.POST.getlist('year_of_completion')[x]
                    # print(request.POST.getlist('degree')[x])
                    # print(request.POST.getlist('college')[x])
                    # print(request.POST.getlist('year_of_completion')[x])
                    educationDoctorModel.objects.create(user=request.user,degree=deg,college=col,year_of_completion=year)
            elif 'degree' not in request.POST and 'college' not in request.POST and 'year_of_completion' not in request.POST:
                user.educationsofdoctor.all().delete()
            if ('hospital_name' in request.POST.keys() and request.POST['hospital_name']) or ('time' in request.POST.keys() and request.POST['time']):
                user.experiencesofdoctor.all().delete()
                for x in range(len(request.POST.getlist('hospital_name'))):  #normalde list[-1] yazıyordu max değeri almak için
                    name=request.POST.getlist('hospital_name')[x]
                    year=request.POST.getlist('time')[x]
                    experienceDoctorModel.objects.create(user=request.user,hospital_name=name,time=year)
            elif 'hospital_name' not in request.POST and 'time' not in request.POST:
                user.experiencesofdoctor.all().delete()
            if ('award_name' in request.POST.keys() and request.POST['award_name']) or ('year' in request.POST.keys() and request.POST['year']):
                user.awardsofdoctor.all().delete()
                for x in range(len(request.POST.getlist('award_name'))):  #normalde list[-1] yazıyordu max değeri almak için
                    award=request.POST.getlist('award_name')[x]
                    ye=request.POST.getlist('year')[x]
                    awardsDoctorModel.objects.create(user=request.user,award_name=award,year=ye)
            elif 'award_name' not in request.POST and 'year' not in request.POST:
                user.awardsofdoctor.all().delete()
    
            if user.email != request.POST["email"]:
                if CustomUserModel.objects.filter(username=request.POST['email']).exists():
                    messages.error(request,"Bu mail adresi başka biri tarafından kulllanılmaktadır",extra_tags="doctorsettings")
                    return redirect("showDoctorProfileSettings")
                user.username=request.POST["email"]
                user.email=request.POST["email"]
                user.save() 
                return redirect("showDoctorProfileSettings")
            else:  
                user.save()   
                messages.success(request,'Profiliniz başarıyla güncellendi!',extra_tags="doctorsettings")
                return redirect("showDoctorProfileSettings")         
        return render(request,"doctor-profile-settings.html",context)               
    return redirect("login")       
  
    


@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def updateSocialMediaDoctor(request):
    item=socialMediaDoctorModel.objects.filter(user=request.user).first()
    if request.method == "POST":
        if item:
            form = socialMediaDoctorForm(request.POST or None,request.FILES or None,instance=item)   
        else:
            form = socialMediaDoctorForm(request.POST or None, files=request.FILES or None)	

        if form.is_valid():
            yazi=form.save(commit=False)
            yazi.user=request.user
            yazi.save()               
            messages.success(request,'Bilgileriniz başarıyla güncellendi!')
            return redirect("updateSocialMediaDoctor")
        else:
            
            messages.error(request,form.errors)
            return redirect("updateSocialMediaDoctor")
    if item:
        form=socialMediaDoctorForm(instance=item)
    else:
        form = socialMediaDoctorForm()
    context={
        "form":form,
        "which_active":"socialmedia"
    }
    return render(request,"social-media.html",context)



# @permission_required('is_staff',login_url="loginAdmin")
# def socialMediaEkleDoctor(request):
#     if request.method == "POST":
#         form = socialMediaDoctorForm(request.POST or None, files=request.FILES or None)		
#         if form.is_valid():
#             yazi=form.save(commit=False)
#             yazi.user=request.user
#             yazi.save()     
#             #form.save_m2m()   
#             messages.success(request,"Bilgiler başarıyla eklenmiştir")
#         else:
#             messages.error(request,"Bilgiler eklenirken hata oluştu.Lütfen alanları gerektiği gibi doldurunuz")
#     form = socialMediaDoctorForm()
#     return render(request=request, template_name="social-media.html.html", context={"form":form})


def clinicImageDelete(request,pk):
    image=get_object_or_404(ClinicImages,pk=pk)
    image.delete()
    messages.success(request,"Fotoğraf başarıyla silinmiştir")
    return redirect(request.META['HTTP_REFERER']) 



def deleteEducation(request,pk): #kullanmıyorum
    edu=get_object_or_404(educationDoctorModel,pk=pk)
    edu.delete()
    messages.success(request,"Model başarıyla silinmiştir")
    return redirect(request.META['HTTP_REFERER']) 




@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def changePasswordDoctor(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()           
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,'Şifreniz başarıyla güncellendi!')
            return redirect("changePasswordDoctor")
        else:
            messages.error(request,"Hata! Lütfen gereken yerleri aşağıda yazıldığı gibi doldurunuz")
            return redirect("changePasswordDoctor")

    form=PasswordChangeForm(request.user)
    context={
        "form":form,
        "error_messages":PasswordChangeForm.error_messages,
        "which_active":"passwordchange"
    }
    return render(request,"doctor-change-password.html",context)

#or 'college' in request.POST.keys() or 'year_of_completion' in request.POST.keys()



@login_required(login_url="login")
@user_passes_test(user_is_patient_check, login_url='login')
def showUserProfileSettings(request):  
    if request.method == "POST":
        form = PatientBasicForm(request.POST or None,request.FILES or None,instance=request.user)   
        if form.is_valid():
            if 'image' not in request.FILES:
                form.save()
            else:                    
                data=form.save(commit=False)             
                data.image=request.FILES["image"] #FILES
                data.save()            
            messages.success(request,'Profiliniz başarıyla güncellendi!')
            return redirect("showUserProfileSettings")
        else:
            # messages.error(request,form.errors)
            messages.error(request,"Bu maile ait kullanıcı mevcut")
            return redirect("showUserProfileSettings")
    form=PatientBasicForm(instance=request.user)
    context={
        "form":form,
        "which_active":"profile"
                        
    }                      
    return render(request,"profile-settings.html",context)
    




@login_required(login_url="login")
@user_passes_test(user_is_patient_check, login_url='login')
def changePasswordPatient(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            user=form.save()           
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,'Şifreniz başarıyla güncellendi!')
            return redirect("changePasswordPatient")
        else:
            messages.error(request,form.errors,extra_tags="invalidchangepassword")
    else:
        form=PasswordChangeForm(user=request.user)
    context={
        "form":form,
        "error_messages":PasswordChangeForm.error_messages,
        "which_active":"passwordchange"
    }
    return render(request,"change-password.html",context)






def showDoctorProfile(request,slug):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    schedules=TimeScheduleModel.objects.filter(doctor=doctor).all()
    for i in schedules:
        if i.date<datetime.date.today():
            i.delete() 
   # clinic_images=doctor.clinicimages.all()
  #  services=doctor.services.split(",")
    specializations=doctor.specializations.split(",")
    educations=educationDoctorModel.objects.filter(user=doctor)
    experiences=experienceDoctorModel.objects.filter(user=doctor)
    awards=awardsDoctorModel.objects.filter(user=doctor)
    comments=CommentModel.objects.filter(doctor=doctor,parent=None,is_published=True)
    comments_count=comments.count()
    if request.user.is_authenticated:
        is_favourite=FavouriteModel.objects.filter(doctor=doctor,patient=request.user)
    else:
        is_favourite=False
    form=CommentModelForm()
   # rating_satisfy=20*doctor.average_star
    none_average_star=5-doctor.average_star  
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 7)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    context={
        "doctor":doctor,
      #  "clinic_images":clinic_images,
      #  "services":services,
        "educations":educations,
        "experiences":experiences,
        "awards":awards,
        "specializations":specializations,
        "comments":comments,
       # "rating_satisfy":rating_satisfy,
        "none_average_star":none_average_star,
        "comments_count":comments_count,
        "is_favourite":is_favourite,
        "average_star":doctor.average_star,
       # "all_comments_count":CommentModel.objects.filter(doctor=doctor,is_published=True).count(),
        "schedules":schedules,
        
    }
    if request.method == "POST":
        form=CommentModelForm(data=request.POST)
        if form.is_valid():    
            data=form.save(commit=False)
            data.comment_user=request.user
            data.doctor=doctor
            if doctor==request.user:
                data.is_published=True
            data.none_star=5-data.star
            if len(data.comment)<130:
                lenData=130-len(data.comment)
                for i in range(lenData):
                    data.comment+=" "
            data.save()
            comments=CommentModel.objects.filter(doctor=doctor,parent=None,is_published=True)
            if data.parent is None:
                average_star=comments.aggregate(Avg('star'))
                if average_star["star__avg"] != None:
                    average_star=int(math.ceil(average_star["star__avg"]))
                else:
                    average_star=0
                doctor.average_star=average_star
                none_average_star=5-doctor.average_star 
                doctor.none_average_star=none_average_star
                doctor.parent_comments_count=comments.count()
            doctor.save()
            if doctor==request.user:
                messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
            else:
                messages.success(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")
            return redirect("showDoctorProfile",slug=slug)
            
        else:
            messages.error(request,"Yorumunuz onaylandıktansss sonra sitemize eklenecektir.",extra_tags="addingcomment")
            return redirect("showDoctorProfile",slug=slug)
      
    return render(request,"doctor-profile.html",context)




def addReplyComment(request,slug,pk):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    parent=get_object_or_404(CommentModel,pk=pk)
    if request.method == "POST":
        form=CommentModelForm(data=request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.comment_user=request.user
            data.doctor=doctor
            data.parent=parent
            data.star=0
            data.none_star=5
            if(doctor==request.user):
                data.is_published=True
                data.save()
                messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
                return redirect("showDoctorProfile",slug=slug)
            data.save()
            messages.success(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")          
            return redirect("showDoctorProfile",slug=slug)
            
        else:
            messages.error(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")
            return redirect("showDoctorProfile",slug=slug)





def addDoctorToFavorites(request,slug):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    if request.method == "GET":
        is_favourite=FavouriteModel.objects.filter(doctor=doctor,patient=request.user)
        if is_favourite:
            is_favourite.all().delete()
            messages.success(request,"Favorilerinizden kaldırılmıştır",extra_tags="favouriteadding")
        else :
            FavouriteModel.objects.create(doctor=doctor,patient=request.user)
            messages.success(request,"Favorilerinize eklenmiştir",extra_tags="favouriteadding")
        return redirect("showDoctorProfile",slug=slug)
    




@login_required(login_url="login")
@user_passes_test(user_is_patient_check, login_url='login')
def showFavouritesOfPatients(request):
    doctors=FavouriteModel.objects.filter(patient=request.user)
    context={
        "doctors":doctors,
        "which_active":"favourites"
    }
    # if request.method == "GET":
    #     is_favourite=FavouriteModel.objects.filter(doctor=doctor,patient=request.user)
    #     if is_favourite:
    #         is_favourite.all().delete()
    #         messages.success(request,"Favorilerinizden kaldırılmıştır",extra_tags="favouriteadding")
    #     else :
    #         FavouriteModel.objects.create(doctor=doctor,patient=request.user)
    #         messages.success(request,"Favorilerinize eklenmiştir",extra_tags="favouriteadding")
    return render(request,"favourites.html",context)
    





@login_required(login_url="login")
@user_passes_test(user_is_patient_check, login_url='login')
def removeFavouritesOfPatients(request,slug):
    if request.method == "GET":
        doctor=get_object_or_404(CustomUserModel,slug=slug)
        FavouriteModel.objects.filter(patient=request.user,doctor=doctor).all().delete()
        messages.success(request,"Favorilerinizden kaldırılmıştır",extra_tags="removefavourite")
    return redirect("showFavouritesOfPatients")
    


@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def showCommentsInDoctorDashboard(request,pk):
    comments=CommentModel.objects.filter(doctor=request.user,is_published=True)
    doctor=request.user
    parent=get_object_or_404(CommentModel,pk=pk)
    if request.method == "POST":
        form=CommentModelForm(data=request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.comment_user=request.user
            data.doctor=doctor
            data.parent=parent
            data.is_published=True
            data.star=0
            data.none_star=5
            data.save()
            messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir",extra_tags="commentaddashboard")          
            return redirect("showCommentsInDoctorDashboard",pk=pk)
            
        else:
            messages.error(request,"Lütfen formu hatasız doldurunuz",extra_tags="commentaddashboard")
            return redirect("showCommentsInDoctorDashboard",pk=pk)

    context={
        "comments":comments,      
    }
    return render(request,"reviews.html",context)



@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def listCommentsAdmin(request):
    #CommentModel.objects.all().delete()
    comments=CommentModel.objects.filter(doctor=request.user,is_published=True)
    context={
        "comments":comments,     
        "which_active":"allComments"   
    }
    return render(request,"reviews.html",context)







def change_active_day(request,day):
    if request.method=='POST' and request.is_ajax():
        try:
            user=get_object_or_404(CustomUserModel,email=request.user.email)
            user.active_day=day
            user.save()
            data ={
                "day":day,
                "timeModels":list(TimeScheduleModel.objects.filter(day=day,doctor=user).all().values()),
            }
            return JsonResponse(data,safe=True)
        except:
           
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})
    
    




def getDayEnglish(day):
    if day == "Pazartesi":
        day="Monday"
    elif day == "Salı":
        day="Tuesday"
    elif day == "Çarşamba":
        day="Wednesday"
    elif day == "Perşembe":
        day="Thursday"
    elif day == "Cuma":
        day="Friday"
    elif day == "Cumartesi":
        day="Saturday"
    elif day == "Pazar":
        day="Sunday"
    return day


def getDayTurkish(day):
    if day == "Monday":
        day="Pazartesi"
    elif day == "Tuesday":
        day="Salı"
    elif day == "Wednesday":
        day="Çarşamba"
    elif day == "Thursday":
        day="Perşembe"
    elif day == "Friday":
        day="Cuma"
    elif day == "Saturday":
        day="Cumartesi"
    elif day == "Sunday":
        day="Pazar"
    return day



def find_date(week_day):
    day=getDayEnglish(week_day)
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    now = weekdays.index(a)
    coming_day_index = weekdays.index(day)
    if coming_day_index<now:
        date = my_date + timedelta(days= 7+coming_day_index-now)
    else:
        date=my_date + timedelta(days= coming_day_index-now)
    # if coming_day_index>=now:
    #     date = my_date - timedelta(days= now - coming_day_index)
    # else:
    #     date = my_date + timedelta(days= 6)
    return date



def get_days_from_today():
    days=[]
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    days.append(a)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    index=weekdays.index(a)
    for i in range(6-index):
        days.append(weekdays[i+index+1])
    for i in range(index):
        days.append(weekdays[i])
    return days


def get_today_name():
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    x=getDayTurkish(a)
    return x



def get_dates():
    dates={
        "Pazartesi":find_date("Pazartesi"),
        "Salı":find_date("Salı"),
        "Çarşamba":find_date("Çarşamba"),
        "Perşembe":find_date("Perşembe"),
        "Cuma":find_date("Cuma"),
        "Cumartesi":find_date("Cumartesi"),
        "Pazar":find_date("Pazar"),
    }
    return dates





@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def schedule(request): 
    days=get_days_from_today()
    dates=get_dates()
    todayDayNameTurkish=get_today_name()
    schedulesAll=TimeScheduleModel.objects.filter(doctor=request.user).all()
    schedules=schedulesAll.filter(date__gte=find_date(todayDayNameTurkish))
    for i in schedulesAll:
        if i.date<datetime.date.today():
            i.delete()   

    # if whichWeek=="this":
    #     schedules=TimeScheduleModel.objects.filter(doctor=request.user,date__gte=find_date("Pazartesi")).filter(date__lte=find_date("Pazar"))
    # elif whichWeek=="next":
    #     schedules=TimeScheduleModel.objects.filter(doctor=request.user,date__gte=find_date("Pazartesi")+timedelta(7)).filter(date__lte=find_date("Pazar")+timedelta(7))
    
    mondayExist=tuesdayExist=wednesdayExist=thursdayExist=fridayExist=saturdayExist=sundayExist="false"
    if schedules:  #count da saydırabilirdin
        for i in schedules:
            if i.day == "Pazartesi":
                mondayExist="true"
            elif i.day == "Salı":
                tuesdayExist="true"
            elif i.day == "Çarşamba":
                wednesdayExist="true"
            elif i.day == "Perşembe":
                thursdayExist="true"
            elif i.day == "Cuma":
                fridayExist="true"
            elif i.day == "Cumartesi":
                saturdayExist="true"
            elif i.day == "Pazar":
                sundayExist="true"

    if request.method == "POST":
       # print(request.POST)
        # print(len(request.POST.getlist('starting_time')))
        if 'starting_time' in request.POST.keys():
            if request.user.timeschedules.count() != 0 :
                for i in request.user.timeschedules.all():
                    if i.day == request.POST['day']:
                        if i.is_paid=="no":
                            i.delete()
            for x in range(len(request.POST.getlist('starting_time'))):  #normalde list[-1] yazıyordu max değeri almak için
                start=request.POST.getlist('starting_time')[x]
                finish=request.POST.getlist('finishing_time')[x]
                if request.POST['duration'] == "":
                    duration=0
                else:
                    duration=request.user.appointment_minute
                # if request.POST['day'] == "":
                #     day="Pazartesi"
                # else:
                #     day=request.POST['day']
                day=request.POST['day']
                if start != "" or finish != "" :
                    xdate=find_date(day)
                    # if whichWeek=="this":
                    #     xdate=find_date(day)
                    # elif whichWeek=="next":
                    #     xdate=find_date(day)+timedelta(7)
                    TimeScheduleModel.objects.create(starting_time=start,finishing_time=finish,doctor=request.user,day=day,duration=duration,date=xdate)
                   
            request.user.active_day=day
            request.user.save()
            messages.success(request,'İşleminiz başarıyla gerçekleşti')
            return redirect("schedule")
    
    context={
        "schedules":schedules,
        "mondayExist":mondayExist,"tuesdayExist":tuesdayExist,"wednesdayExist":wednesdayExist,"thursdayExist":thursdayExist,"fridayExist":fridayExist,"saturdayExist":saturdayExist,"sundayExist":sundayExist,
        "timeSchedule":"asd",
        "which_active":"timeSchedule",
        "days":days,
        "dates":dates
                        
    }                      
    return render(request,"schedule-timings.html",context) 
     

    




@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def listWaitingComments(request):
    comments=CommentModel.objects.filter(doctor=request.user,is_published=False)
    context={
        "comments":comments,  
        "which_active":"waitingComments"
    }
    return render(request,"waiting_comment_list.html",context)



@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def deleteWaitingComment(request,pk):
    comment=get_object_or_404(CommentModel,pk=pk)
    comment.delete()
    messages.success(request,'Yorum başarıyla silindi!',extra_tags="deleteWaitingComment")
    return redirect("listWaitingComments")



@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def acceptWaitingComment(request,pk):
    comment=get_object_or_404(CommentModel,pk=pk)
    comment.is_published=True
    comment.save()
    comments=CommentModel.objects.filter(doctor=request.user,parent=None,is_published=True)
    if comment.parent is None:
        average_star=comments.aggregate(Avg('star'))
        if average_star["star__avg"] != None:
            average_star=int(math.ceil(average_star["star__avg"]))
        else:
            average_star=0
        request.user.average_star=average_star
        none_average_star=5-request.user.average_star 
        request.user.none_average_star=none_average_star
        request.user.parent_comments_count=comments.count()
    request.user.save()
    return redirect("listWaitingComments")




@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def detailWaitingComment(request,pk):
    comment=get_object_or_404(CommentModel,pk=pk)
    context={
        "comment":comment,  
       
    }
    return render(request,"show-comment-detail.html",context)





@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def deleteTimeScheduleModel(request,pk):
    model=get_object_or_404(TimeScheduleModel,pk=pk)
    if model.is_paid=="no" and model.doctor==request.user:
        model.delete()
        messages.success(request,'Randevu saatiniz başarıyla silindi.')
    else:
        messages.error(request,'Aradığınız kriterde randevu bulunamadı.')
    return redirect("schedule")





def getStartingandFinishingTime(request,pk):
    locale.setlocale(locale.LC_ALL, 'tr_TR')
    liste=[]
    engdays=get_days_from_today()
    days=[]
    dates=[]
    for i in engdays:
        days.append(getDayTurkish(i))
    for i in days:
        xdate=find_date(i)
       # adDate=datetime.datetime.strptime(str(xdate), '%Y/%m/%d').strftime('%d %B %Y')
        dates.append(xdate)
    schedules=TimeScheduleModel.objects.filter(doctor_id=pk,date__gte=datetime.date.today(),is_paid="no").all()
    for day in days:
        max_finishing_time=schedules.filter(day=day).order_by("-finishing_time").first()
        min_starting_time=schedules.filter(day=day).order_by("starting_time").first()
        if  max_finishing_time :
            max_finishing_time=max_finishing_time.finishing_time
        else:
            max_finishing_time="-"
        if  min_starting_time :
            min_starting_time=min_starting_time.starting_time
        else:
            min_starting_time="-"
  
        datax ={
            "day":day,
            "max_finishing_time":max_finishing_time,
            "min_starting_time":min_starting_time,               
        }
        liste.append(datax)
   
    data={
        "liste":liste,
        "dates":dates,
        "today":f"{datetime.datetime.now():%d-%m-%y}",
        "day": datetime.datetime.now().strftime("%A"),
    }   
    return JsonResponse(data,safe=True)
  
                



def showAciklamaYazisi(request):
    aciklamaYazisi=indexDoktorlarYaziModel.objects.first()
    context={
        "aciklamaYazisi":aciklamaYazisi,
    }
    return render(request,"aciklamaYazisi.html",context=context)




def showAllDoctors(request):
    doctors=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True)
    context={
        "doctors":doctors,
        "count":doctors.count(),
        "il":""
    }
    return render(request,"searchDoctor.html",context=context)





def save_clinic_images(request):
    if request.method=='POST':   
        my_image=request.FILES.get("file")
        co= ClinicImages.objects.filter(user=request.user).count()
        data=""
        if co <5 :
            data={"accept":"yes"}
            ClinicImages.objects.create(user=request.user,clinic_image=my_image)
        else:
            data={"accept":"no"}
            # messages.error(request,"En fazla 5 adet klinik fotoğrafı yükleyebilirsiniz")
            # return redirect("showDoctorProfileSettings")
        return JsonResponse(data,safe=True)






def searchFilter(request):
    doctors=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True).all()
    il=""
    ilce=""
    cinsiyet=""
    searchKey=""
    min=""
    max=""
    tarih=""
    specialCheckArea=""
    fiyatHatasi=""
    if request.method == "POST":
        if ('kadın' in request.POST.keys() and 'erkek' in request.POST.keys()):
            cinsiyet+="kadin-erkek"
        elif ('kadın' in request.POST.keys()):
            doctors=doctors.filter(gender="female")
            cinsiyet+="kadin"
        elif ('erkek' in request.POST.keys()):
            doctors=doctors.filter(gender="male")
            cinsiyet+="erkek"
        if ('select_specialist' in request.POST.keys()):
            list=request.POST.getlist("select_specialist")
            users = []
            for user in doctors:
                for spe in list:
                    if spe not in specialCheckArea:
                        specialCheckArea+=spe
                    spe=spe.lower()
                    ss=user.specializations
                    ss=ss.lower()
                    if spe in ss:
                        users.append(user.id)
                        break
            doctors=doctors.filter(id__in=users)

        if ('date' in request.POST.keys()):
            date=request.POST.get("date")
            if date !="" and  date!=None:
                tarih=date
                users=[]
                for timeSchedule in TimeScheduleModel.objects.filter(date=date,is_paid="no"):
                    users.append(timeSchedule.doctor.id)
                doctors=doctors.filter(id__in=users)
            else:
                pass

        if ('searchWords' in request.POST.keys()):
            searchWords=request.POST["searchWords"]
            searchKey=searchWords
            lower_map = {
                ord(u'I'): u'ı',
                ord(u'İ'): u'i',
            }
            searchWords=searchWords.translate(lower_map).lower()
            doctors=doctors.filter(specializations__contains=searchWords)  

        if ('minFiyat' in request.POST.keys() or 'maxFiyat' in request.POST.keys()):  
            minFiyat=request.POST['minFiyat']
            maxFiyat=request.POST['maxFiyat']
            if minFiyat !="":
                min=minFiyat
                doctors=doctors.filter(custom_price__gte=minFiyat)
            if maxFiyat !="":
                max=maxFiyat
                doctors=doctors.filter(custom_price__lte=maxFiyat)
            if minFiyat != "" and maxFiyat !="":
                if minFiyat > maxFiyat:
                    fiyatHatasi="Min kısmı max kısmından büyük olamaz"
        

        il=request.POST.get("cityName") 
        ilce=request.POST.get("ilce")
        if "indexPage" in request.POST.keys():
            if il:
                if ilce=="0" or ilce=="" or ilce==None:
                    doctors=doctors.filter(city=il).all()
                    ilce="" 
                else:
                    doctors=doctors.filter(city=il,state=ilce).all()
        else:
            il="Filtre"
    else:
        alanadi=str(request.GET.get("alan"))
        users = []
        for user in doctors:
            alanadi=alanadi.lower()
            ss=user.specializations
            ss=ss.lower()
            if alanadi in ss:
                users.append(user.id)
                break
        doctors = doctors.filter(id__in=users)
        il=alanadi
        
    count=""
    if doctors=="":
        count=0
    else:
        count=doctors.count()
    context={
        "doctors":doctors,
        "count":count,
        "il":il,
        "ilce":ilce,
        "cinsiyet":cinsiyet,
        "specialCheckArea":specialCheckArea,
        "searchKey":searchKey,
        "min":min,
        "max":max,
        "tarih":tarih,
        "fiyatHatasi":fiyatHatasi

    }
    return render(request,"searchDoctor.html",context=context)






@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def doctorDashboard(request):
    today=date.today()
    schedules=TimeScheduleModel.objects.filter(doctor=request.user,is_paid="yes").exclude(status="cancelled").order_by("-pk")
    schedulesToday=TimeScheduleModel.objects.filter(doctor=request.user,is_paid="yes",date=today)
    appointments=appointmentModel.objects.filter(doctor=request.user).all()
    lastAppo=appointments.filter(date__gte=today.replace(day=1))
    doktorKazancLastMonth=0
    komisyonLastMonth=0
    lastMonthData=list()
    for i in lastAppo:
        doktorKazancLastMonth+=i.money
    komisyonLastMonth=doktorKazancLastMonth*(0.2)
    doktorKazancLastMonth-=komisyonLastMonth     
    lastMonthData.append(doktorKazancLastMonth)
    lastMonthData.append(komisyonLastMonth)
    lastMonthData.append(0)
   
    dateToday=datetime.date.today()
    schedulesPk=list()
    data=list()
    doktorKazanc=0
    komisyon=0
    
    for i in appointments:
        doktorKazanc+=i.money
        if i.patient.pk not in schedulesPk:
            schedulesPk.append(i.patient.pk)
    komisyon=doktorKazanc*(0.2)
    doktorKazanc-=komisyon     
    data.append(doktorKazanc)
    data.append(komisyon)
    data.append(0)


    labels=["Hizmet Kazancı","Komisyon","Diğer"]
 
    context={
        "which_active":"doctorDashboard",
        "schedules":schedules,
        "schedulesToday":schedulesToday,
        "appointmentCount":appointments.count(),
        "dateToday":dateToday,
        "schedulesTodayCount":schedulesToday.count(),
        "totalPatientCount":schedulesPk.__len__(),
        "labels":labels,
        "data":data,
        "lastMonthData":lastMonthData
       
    }
    return render(request,"doctor-dashboard.html",context=context)



@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def doctorAppoitments(request):
    details=[]
    address=""
    schedules=TimeScheduleModel.objects.filter(doctor=request.user,is_paid="yes").exclude(status="cancelled").order_by("-pk")
    for i in schedules:
        st=""
        if i.status=="pending":
            st="Bekliyor"
        else:
            st="Onaylandı"

        
        if i.meeting_method == "Whatsapp":
            address=i.patient.iletisimSettings.first().whatsapp
        elif i.meeting_method == "Zoom":
            address=i.patient.iletisimSettings.first().zoom
        elif i.meeting_method == "Skype":
            address=i.patient.iletisimSettings.first().skype
        elif i.meeting_method == "ourSystem":
            address="Kendi Sistemimiz"

        if i.meeting_method=="ourSystem":
            method=""
        else:
            method=i.meeting_method

        ctx={
            "pk":i.pk,
            "date":i.date.strftime(("%d-%m-%Y")),
            "money":i.money,
            "status":st,
            "meeting_method":method,
            "address":address
        }
        details.append(ctx)
    
    context={
        "which_active":"appoitments",
        "schedules":schedules,
        "appoitmentsDoctor":"asd",
        "now":"now",
        "details":details
        
    }
    return render(request,"appointments.html",context=context)



@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def pastAppoitments(request):
    schedules=list()
    details=[]
    filterquery=appointmentModel.objects.filter(doctor=request.user).order_by("-pk")
    print(filterquery.count())
    for i in filterquery:
        if i.meeting_method == "Whatsapp":
            address=i.patient.iletisimSettings.first().whatsapp
        elif i.meeting_method == "Zoom":
            address=i.patient.iletisimSettings.first().zoom
        elif i.meeting_method == "Skype":
            address=i.patient.iletisimSettings.first().skype
        elif i.meeting_method == "ourSystem":
            address="Kendi Sistemimiz"

        if i.meeting_method=="ourSystem":
            method=""
        else:
            method=i.meeting_method
        finishing_time = datetime.datetime.strptime(i.finishing_time, '%H:%M')
        finishing_time=finishing_time.time().strftime("%H:%M")
        now_time=datetime.datetime.now().time().strftime("%H:%M")
        if datetime.date.today() > i.date:
            schedules.append(i)
            ctx={
            "pk":i.pk,
            "date":i.date.strftime(("%d-%m-%Y")),
            "money":i.money,
            "status":"Tamamlandı",
            "meeting_method":method,
            "address":address
            }
            details.append(ctx)
        elif datetime.date.today() == i.date and now_time>finishing_time:
            schedules.append(i)
            ctx={
            "pk":i.pk,
            "date":i.date.strftime(("%d-%m-%Y")),
            "money":i.money,
            "status":"Tamamlandı",
            "meeting_method":method,
            "address":address
            }
            details.append(ctx)

    context={
        "past":"past",
        "schedules":schedules,
        "appoitmentsDoctor":"asd",
        "details":details
        
    }
    return render(request,"appointments.html",context=context)





@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def deletedAppoitments(request):
    details=[]
    address=""
    schedules=deletedAppointmentModel.objects.filter(doctor=request.user).order_by("-pk")
    for i in schedules:
        if i.meeting_method == "Whatsapp":
            address=i.patient.iletisimSettings.first().whatsapp
        elif i.meeting_method == "Zoom":
            address=i.patient.iletisimSettings.first().zoom
        elif i.meeting_method == "Skype":
            address=i.patient.iletisimSettings.first().skype
        elif i.meeting_method == "ourSystem":
            address="Kendi Sistemimiz"

        if i.meeting_method=="ourSystem":
            method=""
        else:
            method=i.meeting_method
        ctx={
            "pk":i.pk,
            "date":i.date.strftime(("%d-%m-%Y")),
            "money":i.money,
            "status":"Reddedildi",
            "meeting_method":method,
            "address":address
        }
        details.append(ctx)
    context={
        "deleted":"deleted",
        "schedules":schedules,
        "appoitmentsDoctor":"asd",
        "details":details
        
    }
    return render(request,"appointments.html",context=context)




@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def doctorPatients(request):
    schedulesPk=list()
    schedules=list()
    sts=appointmentModel.objects.filter(doctor=request.user).all()
    for i in sts:
        if i.patient.pk not in schedulesPk:
            schedulesPk.append(i.patient.pk)
            schedules.append(i)
   
    context={
        "which_active":"patients",
        "schedules":schedules,
        
    }
    return render(request,"my-patients.html",context=context)




@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def doctorInvoices(request):
    
    schedules=appointmentModel.objects.filter(doctor=request.user).all()
    context={
        "which_active":"invoices",
        "schedules":schedules,
        
    }
    return render(request,"invoices.html",context=context)





@login_required(login_url="login")
def invoicesView(request,pk):
    schedule=get_object_or_404(appointmentModel,pk=pk)
    logo=logoModel.objects.all().first()
    if schedule.doctor==request.user or schedule.patient==request.user:
        context={
            "schedule":schedule,
            "logo":logo,
        }
        return render(request,"invoice-view.html",context=context)
    else:
        return render(request,"404.html",{})






def randevuDetayi(request,pk):
    if request.method=='POST' and request.is_ajax():
        try:
            schedule=get_object_or_404(TimeScheduleModel,pk=pk)
            data ={
                "schedule":schedule,
                "pk":pk
            }
            return JsonResponse(data,safe=True)
        except:
           
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})
    



@login_required(login_url="login")
def patientDashboard(request):
    today=date.today()
    schedules=TimeScheduleModel.objects.filter(patient=request.user,is_paid="yes",status="pending")
    appointments=appointmentModel.objects.filter(patient=request.user)
    deletedAppointments=deletedAppointmentModel.objects.filter(patient=request.user)
    context={
        "which_active":"patientDashboard",
        "schedules":schedules,
        "faturalar":appointments,
        "deletedAppointments":deletedAppointments,
        
    }
    return render(request,"patient-dashboard.html",context=context)




def booking(request,slug):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    schedules=TimeScheduleModel.objects.filter(doctor=doctor).all()
    for i in schedules:
        if i.date<datetime.date.today():
            i.delete() 
    engdays=get_days_from_today()
    dates=get_dates()
    days=[]
    for i in engdays:
        days.append(getDayTurkish(i))

    schedules1=schedules.filter(day=days[0],date=find_date(days[0]))
    schedules2=schedules.filter(day=days[1],date=find_date(days[1]))
    schedules3=schedules.filter(day=days[2],date=find_date(days[2]))
    schedules4=schedules.filter(day=days[3],date=find_date(days[3]))
    schedules5=schedules.filter(day=days[4],date=find_date(days[4]))
    schedules6=schedules.filter(day=days[5],date=find_date(days[5]))
    schedules7=schedules.filter(day=days[6],date=find_date(days[6]))

    context={
        "doctor":doctor,
        "days":days,
        "dates":dates,
        "schedules":schedules,
        "schedules1":schedules1,
        "schedules2":schedules2,
        "schedules3":schedules3,
        "schedules4":schedules4,
        "schedules5":schedules5,
        "schedules6":schedules6,
        "schedules7":schedules7,
    }
    return render(request,"booking.html",context=context)




def contact(request):
    if request.method == "POST":
        form = iletişimModelForm(request.POST)
        if form.is_valid(): 
            form.save()
           # print(form.cleaned_data["mesaj"])
            send_mail(
                form.cleaned_data["subject"]+" ( "+form.cleaned_data["fullName"]+" "+ form.cleaned_data["whoIs"]+" )",
                form.cleaned_data["mesaj"]+"\n\n\n ( "+form.cleaned_data["email"]+" )",
                form.cleaned_data["email"],
                ["muhammetay651@gmail.com","muhammet19071340@gmail.com"],
            )
            messages.success(request,"Mesajınız başarıyla tarafımıza iletildi.En kısa sürede sizinle iletişime geçilecektir.Teşekkür ederiz.")
            return redirect("contact")
    form = iletişimModelForm()
    context={
        "form":form,
    }
    return render(request,"iletisim.html",context)






# def defineCallType(request):
#     message=""
#     if request.is_ajax():
#         currentPeer=get_object_or_404(peerInformations,user=request.user)
#         otherPeer=get_object_or_404(peerInformations,peerId=request.GET["otherUserPeerId"])
#         currentPeer.callType=request.GET["whichCall"]
#         otherPeer.callType=request.GET["whichCall"]
#         currentPeer.save()
#         otherPeer.save()
        
#     return HttpResponse(message)





def createPeerIdToUser(request):
    message=""
    if request.is_ajax():
        peer=get_object_or_404(peerInformations,user=request.user)
        if peer:
            peer.peerId=request.GET["peerId"]
            #peer.peerId=request.user.pk
            peer.save()
        else:
            #peerInformations.objects.create(user=request.user,peerId=request.user.pk)
            peerInformations.objects.create(user=request.user,peerId=request.GET["peerId"])
    return HttpResponse(message)



def getOtherUserByPeerId(request):
    if request.is_ajax():
        peer=get_object_or_404(peerInformations,peerId=request.GET["peer"])
        username=""
        if peer.user.is_doctor:
            username=peer.user.get_doctor_name()
        elif peer.user.is_patient:
            username=peer.user.get_full_name()
        data={
            "username":username,
            "type":peer.callType
        }
    return JsonResponse(data)




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




api_key = 'sandbox-dUxCU53r8Mfm7dP3GiznLyBlDIuvQ0qc'
secret_key = 'sandbox-ngWbexjU4ip7C27v5JLuelbCPNojoHPQ'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}

sozlukToken=list()
schedulePk=list()
currentUser=list()

#tüm kontrolleri yap kullanıcı rastgele atama da yapabilir doktor dolu mu boş mu ödeme yapılmış mı hasta girişi var mı hepsini kontrol et
@login_required(login_url="login")
def checkout(request,pk):
    timeSchedule=get_object_or_404(TimeScheduleModel,pk=pk)
    context={
        "timeSchedule":timeSchedule,
        "commentsCount":CommentModel.objects.filter(doctor=timeSchedule.doctor,parent=None,is_published=True).count()
    }
    return render(request,"checkout.html",context)





def makePayment(request,pk):
    method=request.GET.get('method', None)
    meetingMethod=""
    schedulePk.append(pk)
    context = dict()
    currentUser.append(request.user)
    timeSchedule=get_object_or_404(TimeScheduleModel,pk=pk)
    payment_card = {
        'cardHolderName': 'John Doe',
        'cardNumber': '5890040000000016',
        'expireMonth': '12',
        'expireYear': '2030',   
        'cvc': '123',
        'registerCard': '0'
    }   
    if method=="ozel-form":
        payment_card = {
            'cardHolderName': request.POST.get("card_name",None),
            'cardNumber': request.POST.get("card_number",None),
            'expireMonth': request.POST.get("expiry_month",None),
            'expireYear': request.POST.get("expiry_year",None),   
            'cvc': request.POST.get("cvv",None),
            'registerCard': '0'
        }   

    buyer = {
        'id': request.user.pk,
        'name': request.user.first_name,
        'surname': request.user.last_name,
        'gsmNumber': request.user.phone_number,
        'email': request.user.email,
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': request.user.created_date.strftime(("%Y-%m-%d %H:%M:%S")),
        'registrationAddress': request.user.address,
        'ip': get_client_ip(request),
        'city': request.user.state,
        'country':  request.user.country,
        'zipCode': '34732'
    }

    address = {
        'contactName': request.user.get_full_name(),
        'city': request.user.state,
        'country': request.user.country,
        'address': request.user.address,
        'zipCode': '34732'
    }

    basket_items = [
        {
            'id': timeSchedule.pk,
            'name': 'Psikolog Hizmeti',
            'category1': 'Online Hizmet',
            'category2': 'Online Psikolog',
            'itemType': 'PHYSICAL',
            'price': timeSchedule.doctor.custom_price
        },
  
    ]

    asd = {
        'locale': 'tr',
        'conversationId':str(timeSchedule.pk),
        'price': timeSchedule.doctor.custom_price,               #sepet tutarı
        'paidPrice': timeSchedule.doctor.custom_price,       #ödenen tutar
        'currency': 'TRY',
        'installment': '1',
        'basketId': 'B67832',
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/odeme-sonucu",
        "enabledInstallments": ['2', '3', '6', '9'],
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items
    }
    if method=="iyzico":
        meetingMethod=request.GET.get('meetingMethod', None)
        timeSchedule.meeting_method=meetingMethod
        timeSchedule.save()
        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(asd, options)
        content = checkout_form_initialize.read().decode('utf-8')
        json_content = json.loads(content)
        sozlukToken.append(json_content["token"])
        return HttpResponse(json_content["checkoutFormContent"])
    elif method=="ozel-form":
        meetingMethod=request.POST.get("meetingMethod",None)
        timeSchedule.meeting_method=meetingMethod
        asd["callbackUrl"]=""
        payment = iyzipay.Payment().create(asd, options)
        result=payment.read().decode('utf-8')
        sonuc = json.loads(result, object_pairs_hook=list)
        if sonuc[0][1] == 'success':
            timeSchedule.is_paid="yes"
            timeSchedule.status="pending"
            timeSchedule.patient=currentUser[0]
            timeSchedule.duration=timeSchedule.doctor.appointment_minute
            timeSchedule.money=timeSchedule.doctor.custom_price
            currentUser.clear()
            timeSchedule.save()
            context['success'] = 'Başarılı İŞLEMLER'
            return redirect('success',timeSchedule.pk)
        elif sonuc[0][1] == 'failure':
            context['failure'] = 'Başarısız'
            return HttpResponseRedirect(reverse('failure'), context)
        


@require_http_methods(['POST'])
@csrf_exempt
def resultOfPayment(request):           #ödemeden sonra doktora sms gönder
    timeSchedule=get_object_or_404(TimeScheduleModel,pk=schedulePk[0])
    schedulePk.clear()
    context = dict()

    print("result içindeki token -----", sozlukToken)
    asd = {
        'locale': 'tr',
        'conversationId': str(timeSchedule.pk),
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(asd, options)
    print("************************")
    print(type(checkout_form_result))
    resultof = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda
    print("************************")
    sonuc = json.loads(resultof, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    if sonuc[0][1] == 'success':
        timeSchedule.is_paid="yes"
        timeSchedule.status="pending"
        timeSchedule.patient=currentUser[0]
        timeSchedule.duration=timeSchedule.doctor.appointment_minute
        timeSchedule.money=timeSchedule.doctor.custom_price
        currentUser.clear()
        timeSchedule.save()
        context['success'] = 'Başarılı İŞLEMLER'
        return redirect('success',timeSchedule.pk)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)



@login_required(login_url="login")
def success(request,pk):
    schedule=TimeScheduleModel.objects.get(pk=pk)
    context = dict()
    context['success'] = 'İşlem Başarılı'
    context['schedule'] = schedule
    if schedule.doctor == request.user or schedule.patient == request.user:
        template = 'after-payment.html'
        return render(request, template, context)
    else:
        return render(request, "404.html", {})              #404 sayfası yapılacak yapıld




def failure(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'
    template = 'after-payment.html'
    return render(request, template, context)
   





@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def acceptAppointment(request,pk):              #doktora ve hastaya mail at onaylandığına dair smsde olabilir
    timeSchedule=get_object_or_404(TimeScheduleModel,pk=pk)
    timeSchedule.status="confirm"
    timeSchedule.save()
    newAppointment=appointmentModel.objects.create(doctor=timeSchedule.doctor,patient=timeSchedule.patient,duration=timeSchedule.duration,
        day=timeSchedule.day,money=timeSchedule.money,starting_time=timeSchedule.starting_time,finishing_time=timeSchedule.finishing_time,
        date=timeSchedule.date,meeting_method=timeSchedule.meeting_method)
        
    Room.objects.create(first_user=timeSchedule.doctor,second_user=timeSchedule.patient,appointment=newAppointment)    #ödeme yapıldıktan sonra iki kullanıcı arasında oda oluştur
    messages.success(request,'Randevunuzu başarıyla kabul ettiniz!')
    message=" tarihli randevunuz doktorunuz tarafından onaylanmıştır.Lütfen randevu saatinden 5 dk öncesine kadar sistemde hazır bekleyiniz."
    send_mail(
        "Randevunuz doktorunuz tarafından onaylanmıştır."+" ( "+timeSchedule.patient.get_full_name()+" "+ " )",
        str(timeSchedule.date)+" ("+timeSchedule.starting_time+"-"+timeSchedule.finishing_time+")"+message+"\n\n\n",
        footerModel.objects.first().email,
        [timeSchedule.patient.email,],
    )
    

    return redirect("doctorAppoitments")





@login_required(login_url="login")
@user_passes_test(user_is_doctor_check, login_url='login')
def deleteAppointment(request,pk):                  #burada ödemeyi tekrar kullanıcıya yap bildirim gönder
    timeSchedule=get_object_or_404(TimeScheduleModel,pk=pk)
    timeSchedule.is_paid="no"
    timeSchedule.status="cancelled"
    deletedAppointmentModel.objects.create(doctor=timeSchedule.doctor,patient=timeSchedule.patient,duration=timeSchedule.duration,
        day=timeSchedule.day,money=timeSchedule.money,starting_time=timeSchedule.starting_time,finishing_time=timeSchedule.finishing_time,
        date=timeSchedule.date,meeting_method=timeSchedule.meeting_method)
    
    messages.error(request,'Randevuyu reddettiniz.')
    message=" tarihli randevunuz doktorunuz tarafından onaylanmadı.Ödediğiniz seans ücreti sizinle iletişime geçilip tarafınıza iletilecektir.İlginiz için teşekür ederiz."
    send_mail(
        "Randevunuz Onaylanamadı"+" ( "+timeSchedule.patient.get_full_name()+" "+ " )",
        str(timeSchedule.date)+" ("+timeSchedule.starting_time+"-"+timeSchedule.finishing_time+")"+message+"\n\n\n",
        footerModel.objects.first().email,
        [timeSchedule.patient.email,],
    )
    timeSchedule.patient=None
    timeSchedule.save()
    return redirect("doctorAppoitments")





def gizlilikPolitikasi(request):
    return render(request,"gizlilik.html",{})



def kullanimKosullari(request):
    return render(request,"kullanim-kosullari.html",{})




@login_required(login_url="login")
def patientIletisimSettings(request):
    item=iletisimSettingsModel.objects.filter(user=request.user).first()
    if request.method == "POST":
        if item:
            form = iletisimSettingsModelForm(request.POST or None,instance=item)   
        else:
            form = iletisimSettingsModelForm(request.POST or None)	
        if form.is_valid(): 
            model=form.save(commit=False)            
            model.user=request.user
            model.save()
            messages.success(request,"İletişim bilgileriniz başarıyla kaydedildi.")
            return redirect("patientIletisimSettings")
        else:
            messages.error(request,"İletişim bilgileriniz kaydedilemedi.")
            return redirect("patientIletisimSettings")
    if item:
        form = iletisimSettingsModelForm(instance=item)
    else:
        form = iletisimSettingsModelForm()
    context={
        "form":form,
        "which_active":"iletisim",
    }
    return render(request,"patient-iletisim-settings.html",context)