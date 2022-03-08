from datetime import date
from multiprocessing import context
import re
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
from Admin.models import (
    PageModel,
    bottomMenuModel,
    topMenuModel,
)
from Admin.forms import (
    PageModelForm,
    ProfileAdminForm,
)
from onlinedoctor.forms import AlanModelForm, BannerModelForm, FeatureModelForm, AlanYazıModelForm, doctorFeatureIndexModelForm, footerModelForm, indexDoktorYaziModelForm, logoModelForm
from onlinedoctor.models import CommentModel, CustomUserModel, TimeScheduleModel, alanModel, alanYazilarModel, appointmentModel, bannerModel, deletedAppointmentModel, doctorFeatureIndexModel, featureModel, footerModel, indexDoktorlarYaziModel, logoModel
# Create your views here.
from django.core.mail import EmailMessage


@permission_required('is_staff',login_url="loginAdmin")
def indexAdmin(request):
    #alanModel.objects.all().delete()
    #indexDoktorlarYaziModel.objects.all().delete()
    doctors_count=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True,is_active=True).count()
    patients_count=CustomUserModel.objects.filter(is_patient=True,is_active=True).count()
    appointments=appointmentModel.objects.all()


    today=date.today()
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
    data=list()
    doktorKazanc=0
    komisyon=0
    totalMoney=0
    for i in appointments:
        doktorKazanc+=i.money
        totalMoney+=i.money
    komisyon=doktorKazanc*(0.2)
    doktorKazanc-=komisyon     
    data.append(doktorKazanc)
    data.append(komisyon)
    data.append(0)
    labels=["Doktor Kazancı","Sizin Kazancınız","Diğer"]


    doctors=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True,is_active=True).order_by("average_star")[:5]
    patients=CustomUserModel.objects.filter(is_patient=True,is_active=True)[:5]
    schedules=TimeScheduleModel.objects.filter(is_paid="yes")
    context={
        "active":"anasayfa",
        "doctors_count":doctors_count,
        "patients_count":patients_count,
        "appointmentsCount":appointments.count(),
        "totalMoney":totalMoney,
        "doctors":doctors,
        "patients":patients,
        "schedules":schedules,
        "labels":labels,
        "data":data,
        "lastMonthData":lastMonthData

    }
    return render(request,"indexAdmin.html",context)




def loginAdmin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)		
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                print("başarılı")
                return redirect("indexAdmin")
            else:
                messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
        else:
            messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
    form = AuthenticationForm()
    return render(request=request, template_name="loginAdmin.html", context={"form":form})



def logoutAdmin(request):
    logout(request)
    return redirect("loginAdmin")





@permission_required('is_staff',login_url="loginAdmin")
def showPagesAdmin(request):
    pages=PageModel.objects.all()
    return render(request,"pagesAdmin.html",{"pages":pages,"active":"meta_ayarlar"})






@permission_required('is_staff',login_url="loginAdmin")
def createPageModel(request):
    if request.method == "POST":
        form = PageModelForm(request.POST or None)		
        if form.is_valid():
            form.save()
            messages.success(request,'Sayfa Modeliniz başarıyla oluşturuldu')
            return redirect("createPageModel")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    form = PageModelForm()
    return render(request=request, template_name="pageCreateUpdateAdmin.html", context={"form":form})





@permission_required('is_staff',login_url="loginAdmin")
def updatePageModel(request,pk):
    page=get_object_or_404(PageModel,pk=pk)
    form = PageModelForm(instance=page)
    if request.method == "POST":
        form = PageModelForm(request.POST or None,instance=page)		
        if form.is_valid():
            form.save()
            messages.success(request,'Sayfa Modeliniz başarıyla güncellendi')
            return redirect("updatePageModel",pk)
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="pageCreateUpdateAdmin.html", context={"form":form,"page_pk":pk})





@permission_required('is_staff',login_url="loginAdmin")
def deletePage(request,pk):
    page=get_object_or_404(PageModel,pk=pk)
    page.delete()
    messages.success(request,"Sayfa modeli başarıyla silinmiştir")
    return redirect(request.META['HTTP_REFERER']) 




@permission_required('is_staff',login_url="loginAdmin")
def listWaitingDoctors(request):
    doctors=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=False)
    return render(request,"waitingDoctorsAdmin.html",{"doctors":doctors,"active":"listOfWatingDoctors"})





@permission_required('is_staff',login_url="loginAdmin")   
def acceptWatiingDoctor(request,slug):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    doctor.is_active=True           #biz onaylarsak mail adreside otomatik onaylanmış oluyor
    doctor.doctor_okey=True
    doctor.save()
    mail_subject = 'Doktor hesabınız aktif edildi.'
    to_email = doctor.email
    message="Hesabınız yöneticimiz tarafından aktif edilmiştir.Sistemimizi kullanmaya başlayabilirsiniz."
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    messages.success(request,"Doktor başarıyla kaydedilmiştir")
    return redirect("listWaitingDoctors") 




@permission_required('is_staff',login_url="loginAdmin")
def deleteWaitingDoctor(request,pk):
    doctor=get_object_or_404(CustomUserModel,pk=pk)
    doctor.delete()
    messages.success(request,"Kullanıcı başarıyla silinmiştir")
    return redirect(request.META['HTTP_REFERER']) 





@permission_required('is_staff',login_url="loginAdmin")
def allDoctors(request):
    doctors=CustomUserModel.objects.filter(is_doctor=True,doctor_okey=True,is_active=True)
    return render(request,"doctorsAdmin.html",{"doctors":doctors,"active":"allDoctors"})




@permission_required('is_staff',login_url="loginAdmin")
def profileAdminShow(request):
    if request.method == "POST":
        instance = request.user
        form = ProfileAdminForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            data=form.save(commit=False)      
            email_exists = CustomUserModel.objects.filter(email=form.cleaned_data.get('email')).exclude(email=request.user.email)
            if email_exists:
                messages.error(request,"Bu email başka bir kullanıcı tarafından kullanılmaktadır.Lütfen kendi mail adresinizi giriniz.")
                return redirect('profileAdminShow') 
            data.username=form.cleaned_data.get('email')
            data.save()
            messages.success(request,"Bilgileriniz başarıyla güncellendi.")
            return redirect('profileAdminShow')
        else:
            messages.error(request,form.errors)
            return render(request,"profileSettingsAdmin.html",{"form":form,})
    form=ProfileAdminForm(instance=request.user)
    context={"form":form,}
    return render(request,"profileSettingsAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def changePasswordAdmin(request):
    if request.method == "POST":
        passwordform = PasswordChangeForm(request.user,request.POST)
        if passwordform.is_valid():
            user=passwordform.save()           
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,'Şifreniz başarıyla güncellendi!')
            return redirect("profileAdminShow")
        else:
            messages.error(request,passwordform.errors)
            form=ProfileAdminForm(instance=request.user)
            context={"form":form,"passwordform":passwordform}
            return render(request,"profileSettingsAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def allPatients(request):
    patients=CustomUserModel.objects.filter(is_patient=True)
    return render(request,"patientsAdmin.html",{"patients":patients,"active":"allPatients"})





@permission_required('is_staff',login_url="loginAdmin")
def showDoctorAdmin(request,slug):
    doctor=get_object_or_404(CustomUserModel,slug=slug)
    active=""
    if doctor.is_doctor:
        active="allDoctors"
    elif doctor.is_patient:
        active="allPatients"
    return render(request,"doctorProfileAdmin.html",{"doctor":doctor,"active":active})



@permission_required('is_staff',login_url="loginAdmin")
def appoitmentsAdmin(request):
    schedules=appointmentModel.objects.all()
    context={
        "schedules":schedules,
        "active":"allAppoitments",
        "appointmentType":"Randevular"
    }
    return render(request,"appointment_list_admin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deletedAppoitmentsAdmin(request):
    schedules=deletedAppointmentModel.objects.all()
    context={
        "schedules":schedules,
        "active":"deletedAppoitments",
        "appointmentType":"Onaylanmayan Randevular"
    }
    return render(request,"appointment_list_admin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def specialitiesAdmin(request):
    if request.method == "POST":
        form = AlanModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()      
            messages.success(request,"Alan başarıyla eklendi.")
            return redirect('specialitiesAdmin')
        else:
            messages.error(request,form.errors)
            alanlar=alanModel.objects.all()
            context={
                "alanlar":alanlar,
                "active":"allSpecialities",
                "specialitiesPage":"asd",
                "form":form
            }
            return render(request,"specialitiesAdmin.html",context)
    form=AlanModelForm()
    alanlar=alanModel.objects.all()
    context={
        "alanlar":alanlar,
        "active":"allSpecialities",
        "specialitiesPage":"asd",
        "form":form
    }
    return render(request,"specialitiesAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def updateSpecialist(request,pk):
    instance=get_object_or_404(alanModel,pk=pk)
    if request.method == "POST":
        form = AlanModelForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            form.save()      
            messages.success(request,"Alan başarıyla güncellendi.")
            return redirect('updateSpecialist')
        else:
            messages.error(request,form.errors)
            alanlar=alanModel.objects.all()
            context={
                "alanlar":alanlar,
                "active":"allSpecialities",
                "specialitiesPage":"asd",
                "form":form
            }
            return render(request,"specialitiesAdmin.html",context)
    form=AlanModelForm(instance=instance)
    alanlar=alanModel.objects.all()
    context={
        "alanlar":alanlar,
        "active":"allSpecialities",
        "specialitiesPage":"asd",
        "form":form
    }
    return render(request,"specialitiesAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def reviewsAdmin(request):
    reviews=CommentModel.objects.filter(parent=None,is_published=True)
    print(reviews.count())
    context={
        "reviews":reviews,
        "active":"allReviews",
        "reviewsAdmin":"das"
    }
    return render(request,"reviewsAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def deleteReview(request,pk):
    review=get_object_or_404(CommentModel,pk=pk)
    review.delete()
    messages.success(request,"Yorum başarıyla silindi")
    return redirect("reviewsAdmin")



@permission_required('is_staff',login_url="loginAdmin")
def deleteSpecial(request,pk):
    spe=get_object_or_404(alanModel,pk=pk)
    spe.delete()
    messages.success(request,"Alan başarıyla silindi")
    return redirect("specialitiesAdmin")





@permission_required('is_staff',login_url="loginAdmin")
def allBannersAdmin(request):
    banners=bannerModel.objects.all()
    context={
        "banners":banners,
        "active":"bannersAdmin",
      
    }
    return render(request,"allBannersAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def createBannerModel(request):
    if request.method == "POST":
        form = BannerModelForm(request.POST or None)		
        if form.is_valid():
            bannerModel.objects.all().delete()
            form.save()
            messages.success(request,'Banner başarıyla oluşturuldu')
            return redirect("allBannersAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    form = BannerModelForm()
    return render(request=request, template_name="bannerAdminCreateUpdate.html", context={"form":form})






@permission_required('is_staff',login_url="loginAdmin")
def updateBannerModel(request,pk):
    banner=get_object_or_404(bannerModel,pk=pk)
    form = BannerModelForm(instance=banner)
    if request.method == "POST":
        form = BannerModelForm(request.POST or None,instance=banner)		
        if form.is_valid():
            form.save()
            messages.success(request,'Banner başarıyla güncellendi')
            return redirect("allBannersAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="bannerAdminCreateUpdate.html", context={"form":form,"updateBanner":pk})




@permission_required('is_staff',login_url="loginAdmin")
def deleteBanner(request,pk):
    banner=get_object_or_404(bannerModel,pk=pk)
    banner.delete()
    messages.success(request,"Banner başarıyla silindi")
    return redirect("allBannersAdmin")




@permission_required('is_staff',login_url="loginAdmin")
def alanYaziListeleAdmin(request):
    alanYazilar=alanYazilarModel.objects.all()
    context={
        "alanYazilar":alanYazilar,
        "active":"alanYazilarAdmin",
      
    }
    return render(request,"alanYazilarAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def createAlanYaziModel(request):
    if request.method == "POST":
        form = AlanYazıModelForm(request.POST or None)		
        if form.is_valid():
            alanYazilarModel.objects.all().delete()
            form.save()
            messages.success(request,'Alan yazısı başarıyla oluşturuldu')
            return redirect("alanYaziListeleAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    form = AlanYazıModelForm()
    return render(request=request, template_name="alanYaziCreateupdateAdmin.html", context={"form":form,"active":"alanYazilarAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def updateAlanYaziModel(request,pk):
    alan=get_object_or_404(alanYazilarModel,pk=pk)
    form = AlanYazıModelForm(instance=alan)
    if request.method == "POST":
        form = AlanYazıModelForm(request.POST or None,instance=alan)		
        if form.is_valid():
            form.save()
            messages.success(request,'Alan Yazısı başarıyla güncellendi')
            return redirect("alanYaziListeleAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="alanYaziCreateupdateAdmin.html", context={"form":form,"updateAlanYazisiPk":pk,"active":"alanYazilarAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def deleteAlanYazi(request,pk):
    banner=get_object_or_404(alanYazilarModel,pk=pk)
    banner.delete()
    messages.success(request,"Alan yazısı başarıyla silindi")
    return redirect("alanYaziListeleAdmin")







@permission_required('is_staff',login_url="loginAdmin")
def allIndexYaziAdmin(request):
    yazilar=indexDoktorlarYaziModel.objects.all()
    if yazilar:
        pass
    else:
        indexDoktorlarYaziModel.objects.create(yazi="index yazisi gelecek",top_title="üst başlık",bottom_title="alt başlık")
    context={
        "yazilar":yazilar,
        "active":"indexYaziAdmin",
      
    }
    return render(request,"allYaziındexAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def updateIndexYaziModel(request,pk):
    yazi=get_object_or_404(indexDoktorlarYaziModel,pk=pk)
    form = indexDoktorYaziModelForm(instance=yazi)
    if request.method == "POST":
        form = indexDoktorYaziModelForm(request.POST or None,instance=yazi)		
        if form.is_valid():
            form.save()
            messages.success(request,'Açıklama Yazısı başarıyla güncellendi')
            return redirect("allIndexYaziAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="indexYaziCreateAndUpdate.html", context={"form":form,"pk":pk,"active":"indexYaziAdmin"})





@permission_required('is_staff',login_url="loginAdmin")
def updateFooterModelAdmin(request):
    footer=footerModel.objects.all().first()
    if footer:
        pass
    else:
        footerModel.objects.create(aciklamaYazisi="footer açıklama yazısı")
    form = footerModelForm(instance=footer)
    if request.method == "POST":
        form = footerModelForm(request.POST or None,request.FILES or None,instance=footer)		
        if form.is_valid():
            form.save()
            messages.success(request,'Footer başarıyla güncellendi')
            return redirect("updateFooterModelAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="footerUpdateAdmin.html", context={"form":form,"active":"footerAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def updateDoctorFeatureIndexAdmin(request):
    feature=doctorFeatureIndexModel.objects.all().first()
    if feature:
        pass
    else:
        feature=doctorFeatureIndexModel.objects.create(yazi="açıklama yazısı")
    form = doctorFeatureIndexModelForm(instance=feature)
    if request.method == "POST":
        form = doctorFeatureIndexModelForm(request.POST or None,request.FILES or None,instance=feature)		
        if form.is_valid():
            form.save()
            messages.success(request,'Doktor özellikleri yazı ve image kısmı başarıyla güncellendi')
            return redirect("updateDoctorFeatureIndexAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="featureDoctorIndexAdmin.html", context={"form":form,"active":"featureDoctorAdmin"})








@permission_required('is_staff',login_url="loginAdmin")
def allFeaturesAdmin(request):
    features=featureModel.objects.all()
    context={
        "features":features,
        "active":"featuresIndexAdmin",
      
    }
    return render(request,"allFeatureIndexAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def createFeatureIndexAdmin(request):
    if request.method == "POST":
        form = FeatureModelForm(request.POST or None,request.FILES or None)		
        if form.is_valid():
            form.save()
            messages.success(request,'Özellik başarıyla oluşturuldu')
            return redirect("allFeaturesAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    form = FeatureModelForm()
    return render(request=request, template_name="featuresDoctorCreateUpdate.html", context={"form":form,"active":"featureDoctorAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def updateFeatureIndexAdmin(request,pk):
    feature=get_object_or_404(featureModel,pk=pk)
    form = FeatureModelForm(instance=feature)
    if request.method == "POST":
        form = FeatureModelForm(request.POST or None,request.FILES or None,instance=feature)		
        if form.is_valid():
            form.save()
            messages.success(request,'Özellik başarıyla güncellendi')
            return redirect("allFeaturesAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="featuresDoctorCreateUpdate.html", context={"form":form,"pk":pk,"active":"featureDoctorAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def deleteFeatureIndexAdmin(request,pk):
    feature=get_object_or_404(featureModel,pk=pk)
    feature.delete()
    messages.success(request,"Özellik başarıyla silindi")
    return redirect("allFeaturesAdmin")



@permission_required('is_staff',login_url="loginAdmin")
def updatelogoModelAdmin(request):
    logo=logoModel.objects.all().first()
    if logo:
        pass
    else:
        logoModel.objects.create(anaLogo="static/assets/img/logo.png",footerLogo="static/assets/img/footer-logo.png")
    form = logoModelForm(instance=logo)
    if request.method == "POST":
        form = logoModelForm(request.POST or None,request.FILES or None,instance=logo)		
        if form.is_valid():
            form.save()
            messages.success(request,'Logolar başarıyla güncellendi')
            return redirect("updatelogoModelAdmin")
        else:
            messages.error(request,"LÜtfen formu gerektiği gibi doldurunuz")
    return render(request=request, template_name="logoUpdateAdmin.html", context={"form":form,"active":"logoAdmin"})




@permission_required('is_staff',login_url="loginAdmin")
def allInvoiceReportsAdmin(request):
    faturalar=appointmentModel.objects.all()
    context={
        "faturalar":faturalar,
        "active":"faturalar",
      
    }
    return render(request,"faturalarAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def viewInvoiceDetailAdmin(request,pk):
    fatura=get_object_or_404(appointmentModel,pk=pk)
    logo=logoModel.objects.all().first()
    context={
        "fatura":fatura,
        "active":"faturalar",
        "logo":logo
    }
    return render(request,"fatura-detay-admin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def settingsPatientMenuAdmin(request):
    allMenu=""
    bottomMenus=""
    type=request.GET.get("type",None)
    sendType=""
    if type == "hasta":
        sendType="Hasta"
        allMenu=topMenuModel.objects.filter(userType="patient")
        bottomMenus=bottomMenuModel.objects.filter(userType="patient")
    elif type == "doktor":
        sendType="Doktor"
        allMenu=topMenuModel.objects.filter(userType="doctor")
        bottomMenus=bottomMenuModel.objects.filter(userType="doctor")
    elif type == "nouser":
        sendType="Giriş Yapılmadan"
        allMenu=topMenuModel.objects.filter(userType="nouser")
        bottomMenus=bottomMenuModel.objects.filter(userType="nouser")   
    menuler=[*allMenu, *bottomMenus] 
    menuler.sort(key=lambda x: x.menuType, reverse=True)
    context={
        "menuler":allMenu,
        "sendType":sendType,
        "type":type
        
    }
    return render(request,"menuSettingsAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def patientMenuAdminEkle(request):
    sendUrl=""
    if request.method == "POST":
        name=request.POST["name"]
        url=request.POST["url"]
        type=request.POST["userType"]
        if type == "hasta":
            type="patient"
            sendUrl="/nedmin/menu-ayarlari-admin?type=hasta"
        elif type == "doktor":
            type="doctor"
            sendUrl="/nedmin/menu-ayarlari-admin?type=doktor"
        elif type == "nouser":
            type="nouser"
            sendUrl="/nedmin/menu-ayarlari-admin?type=nouser"
        menu=request.POST["menuType"]
        menuSira=request.POST["menuSira"]
        if menu == "ust-menu":
            if 'objPk' in request.POST.keys():
                pkOfObject=request.POST["objPk"]
                updatedObject=get_object_or_404(topMenuModel,pk=pkOfObject)
                updatedObject.name=name
                updatedObject.url=url
                updatedObject.menuSira=menuSira
                updatedObject.save()
                messages.success(request,"Üst Menü başarıyla güncellendi")
            else:
                topMenuModel.objects.create(name=name,url=url,userType=type,menuSira=menuSira)
                messages.success(request,"Üst Menü başarıyla oluşturuldu")
            return redirect(sendUrl)
        elif menu == "alt-menu":
            topMenu=get_object_or_404(topMenuModel,pk=request.POST["topMenu"])
            if 'objPk' in request.POST.keys():
                pkOfObject=request.POST["objPk"]
                updatedObject=get_object_or_404(bottomMenuModel,pk=pkOfObject)
                updatedObject.name=name
                updatedObject.url=url
                updatedObject.topMenu=topMenu
                updatedObject.menuSira=menuSira
                updatedObject.save()
                messages.success(request,"Alt Menü başarıyla güncellendi")
            else:
                bottomMenuModel.objects.create(name=name,url=url,userType=type,topMenu=topMenu,menuSira=menuSira)
                messages.success(request,"Alt Menü başarıyla oluşturuldu")
            return redirect(sendUrl)

    type=request.GET.get("tip",None)
    menu=request.GET.get("menu",None)
    objPk=request.GET.get("pk",None)
    obj=""
    if objPk:
        if menu == "alt-menu":
            obj=get_object_or_404(bottomMenuModel,pk=objPk)
        elif menu == "ust-menu":
            obj=get_object_or_404(topMenuModel,pk=objPk)

    ustMenuler=""
    if type=="hasta":
        ustMenuler=topMenuModel.objects.filter(userType="patient")
    elif type=="doktor":
        ustMenuler=topMenuModel.objects.filter(userType="doctor")
    elif type=="nouser":
        ustMenuler=topMenuModel.objects.filter(userType="nouser")
    context={
       "type":type,
       "menu":menu,
       "ustMenuler":ustMenuler,
       "obj":obj
        
    }
    return render(request,"menuEkleAdmin.html",context)



def deleteMenu(request,pk,str):
    if str=="Üst Menü":
        obj=get_object_or_404(topMenuModel,pk=pk)
        obj.delete()
        messages.success(request,"Üst Menü başarıyla silindi")
    elif str=="Alt Menü":
        obj=get_object_or_404(bottomMenuModel,pk=pk)
        obj.delete()
        messages.success(request,"Alt Menü başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 