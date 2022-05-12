import calendar
import datetime
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
import json
from django.shortcuts import get_object_or_404
from config.settings import base
from django.db.models.functions import ExtractYear
from django.utils.timezone import now
from datetime import date, timedelta
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from PIL import Image
from django.core.files.storage import default_storage as storage
# from .views import getDayEnglish

# Create your models here.



class bannerModel(models.Model):
    top_title=models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    bottom_title=models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="banner"
        verbose_name = 'Banner'
        verbose_name_plural = 'Banner'





class alanModel(models.Model):
    name=models.CharField(max_length=250,blank=False,null=False)
    image=models.ImageField(
        upload_to="alan_images",
    )
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="alan"
        verbose_name = 'Alan'
        verbose_name_plural = 'Alanlar'



class alanYazilarModel(models.Model):
    top_title=models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    bottom_title=models.TextField(
        max_length=250,
        blank=False,
        null=False
    )
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="alanYazi"
        verbose_name = 'Alan Yazı'
        verbose_name_plural = 'Alan Yazıları'





class CustomUserModel(AbstractUser):
    STATUS = (
        ("female" , "Kadın"),
        ("male" , "Erkek")
    )
    STATUS_BLOOD = (
        ("A-" , "A-"),
        ("A+" , "A+"),
        ("B-" , "B-"),
        ("B+" , "B+"),
        ("AB-" , "AB-"),
        ("AB+" , "AB+"),
        ("0-" , "0-"),
        ("0+" , "0+"),
    )
    is_doctor=models.BooleanField(default=False)
    doctor_okey=models.BooleanField(default=False)
    # doctor_file=models.FileField(
    #     upload_to="doctor_images",blank=True,null=True,default='avatar/no-avatar.png'
    # )
    is_patient=models.BooleanField(default=False)
    define_profession=models.CharField(max_length=450,blank=False,null=False,default="")
    slug=AutoSlugField(populate_from="get_full_name",unique=True)  #düzgün çalaışıyormu kontrol et
    gender=models.CharField(max_length=10,choices=STATUS,default="None",verbose_name="Cinsiyetiniz",blank=True,null=True)            #gender ve date birth düzeltilecek
    blood_group=models.CharField(max_length=10,choices=STATUS_BLOOD,default="None",verbose_name="Kan Grubunuz",blank=True,null=True)    
    date_of_birth=models.DateField(blank=True,null=True)
    email=models.EmailField(max_length=250,blank=False,null=False,unique=True)
    phone_number=models.CharField(max_length=250,blank=False,null=False)
    unvan=models.CharField(max_length=250,blank=False,null=False,default="")
    image=models.ImageField(
        upload_to="doctor_images",blank=True,null=True,default='avatar/no-avatar.png'
    )
    file=models.FileField(
        upload_to="doctors_file",blank=True,null=True
    )
    kimlik=models.FileField(
        upload_to="doctors_file",blank=True,null=True
    )
    about=models.TextField(blank=True,null=True,default="")
    clinic_name=models.CharField(max_length=250,blank=True,null=True,default="")
    clinic_address=models.CharField(max_length=250,blank=True,null=True,default="")
    clinic_image=models.ImageField(                                     #çoklu foto desteği gelecek
        upload_to="doctor_images/clinic_images",blank=True,null=True
    )
    city=models.CharField(max_length=50,blank=True,null=True,default="")              # il adı döndürür 
    cityCode=models.CharField(max_length=50,blank=True,null=True,default="")              #select value değeri döndürü 1 2 gibi
    state=models.CharField(max_length=100,blank=True,null=True,default="") 
    country=models.CharField(max_length=50,blank=True,null=True,default="Türkiye")                   #ilçe
    address=models.CharField(max_length=450,blank=True,null=True,default="")
    is_free=models.BooleanField(default=True)
    custom_price=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    parent_comments_count=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    appointment_minute=models.PositiveSmallIntegerField(blank=True,null=True)
    services=models.CharField(max_length=750,blank=True,null=True,default="")
    specializations=models.CharField(max_length=750,blank=True,null=True,default="")  
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    active_day=models.CharField(max_length=50,blank=True,null=True,default="Pazartesi")       
    online=models.CharField(max_length=10,blank=True,null=True,default="offline")
    is_active_now=models.BooleanField(default=False)
    


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img=Image.open(self.image.path)
    #     resized_image = img.resize((300, 300), Image.ANTIALIAS)
    #     fh = storage.open(self.image.name, "wb")
    #     picture_format = 'png'
    #     resized_image.save(fh, picture_format)
    #     fh.close()        
    #     # output_size = (300,300)
    #     # img.thumbnail(output_size)
    #     # img.save(self.image.path)



    @property
    def countOfPublishedComments(self):
        return CommentModel.objects.filter(parent=None,is_published=True,doctor=self).count()

    
    def get_doctor_name(self):
        return self.unvan+" "+self.get_full_name()

    
    def get_clinic_images(self):
        return self.clinicimages.all()

    
    def get_services(self):
        return self.services.split(",")
    
    def get_specializations(self):
        return self.specializations.split(",")
    
    def get_rating_satisfy(self):
        return 20*self.average_star


    def hasSocialMedia(self):
        socialAccount=socialMediaDoctorModel.objects.filter(user=self).count()
        if socialAccount>0:
           return True
        else:
            return False


    def get_social_medias_for_doctors(self):
        return get_object_or_404(socialMediaDoctorModel,user=self)


    def get_all_comments_count(self):
        return CommentModel.objects.filter(doctor=self,is_published=True).count()


    def get_available_date(self):
        dateof=""
        tomorrow=datetime.date.today()+datetime.timedelta(days=1)
        schedules=TimeScheduleModel.objects.filter(doctor=self,is_paid="no",date__gte=datetime.date.today()).all()
        if schedules:
            if schedules.first().date==datetime.date.today():
                dateof="Bugün için müsait"    
            elif schedules.first().date==tomorrow:
                dateof="Yarın için müsait"
            else:
                dateof=schedules.first().date
                dateof=dateof.strftime("%d/%m/%Y")+" taihinde müsait"
                return dateof
        else:
            dateof="Bu hafta için müsait değil"
        return dateof


    

    def calculate_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


    class Meta:
        db_table="customUser"
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'




class ClinicImages(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="clinicimages")
    clinic_image=models.ImageField(                                     #çoklu foto desteği gelecek
        upload_to="doctor_images/clinic_images",blank=True,null=True
    )



class educationDoctorModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="educationsofdoctor")  
    degree=models.CharField(max_length=250,blank=True,null=True)   
    college=models.CharField(max_length=250,blank=True,null=True)     #eksik alanlar var devamında eklersin
    year_of_completion=models.CharField(max_length=250,blank=True,null=True)   
    

    class Meta:
        db_table="degreeDoctor"
        verbose_name ="Eğitim"  
        verbose_name_plural ="Eğitimler"

    def __str__(self):
        return self.college





class experienceDoctorModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="experiencesofdoctor")
    hospital_name=models.CharField(max_length=250,blank=True,null=True)   
    time=models.CharField(max_length=250,blank=True,null=True)     #eksik alanlar var devamında eklersin
   
    

    class Meta:
        db_table="experienceDoctor"
        verbose_name ="Tecrübe"  
        verbose_name_plural ="Tecrübeler"

    def __str__(self):
        return self.hospital_name


class awardsDoctorModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="awardsofdoctor")
    award_name=models.CharField(max_length=250,blank=True,null=True)   
    year=models.CharField(max_length=250,blank=True,null=True)     #eksik alanlar var devamında eklersin
  
    

    class Meta:
        db_table="awardsDoctor"
        verbose_name ="Ödül"  
        verbose_name_plural ="Ödüller"

    def __str__(self):
        return self.award_name




class socialMediaDoctorModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="social_media")  
    facebook=models.CharField(max_length=250,blank=True,null=True)   
    twitter=models.CharField(max_length=250,blank=True,null=True)   
    instagram=models.CharField(max_length=250,blank=True,null=True)   
    pinterest=models.CharField(max_length=250,blank=True,null=True)   
    linkedin=models.CharField(max_length=250,blank=True,null=True)   
    youtube=models.CharField(max_length=250,blank=True,null=True)    
    
    class Meta:
        db_table="socialMediaDoctor"
        verbose_name ="Sosyal Medya"  
        verbose_name_plural ="Sosyal Medya Hesapları"

    def __str__(self):
        return self.user.email







class CommentModel(models.Model):
    doctor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="all_comments") 
    comment_user= models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="his_comments")
    is_recommend=models.BooleanField(default=False)
    star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_star=models.PositiveSmallIntegerField(blank=True,null=True,default=5)
    comment=models.TextField(blank=True,null=True,default="")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)
    is_published=models.BooleanField(default=False)

    @property
    def children(self):
        return CommentModel.objects.filter(parent=self,is_published=True).order_by("created_date").all()
    

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    
    @property
    def lengthOfCommentIsLess(self):
        if len(self.comment)<135:
            return True
        return False
    

    @property
    def addSpaceToComment(self):
        strLen=135-len(self.comment)
        str=""
        for i in range(strLen):
            str+="  "
        return str

    class Meta:
        ordering = ('-created_date',)
        db_table="comment"
        verbose_name ="Yorum"  
        verbose_name_plural ="Yorumlar"

    def __str__(self):
        return self.comment_user.email





# from django.contrib.postgres.fields import ArrayField       *******   POSTGRESQL geçiş yaptığında bir incele *************
# class Board(models.Model):
#     pieces = ArrayField(ArrayField(models.IntegerField()))
# However, it can only be available when using PostgreSQL for the database.




class FavouriteModel(models.Model):
    doctor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="patients_favourite") 
    patient= models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="favourites")
    class Meta:
        db_table="favourites"
        verbose_name ="Favori"  
        verbose_name_plural ="Favoriler"

    def __str__(self):
        return self.doctor.get_full_name()




class TimeScheduleModel(models.Model):
    DURATION = (
        (0 , "-"),
        (15 , "15 dk"),
        (30 , "30 dk"),
        (45 , "45 dk"), 
        (60 , "60 dk"),
       
    )
    doctor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="timeschedules")  
    patient=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,null=True,blank=True)  
    duration=models.PositiveSmallIntegerField(choices=DURATION,default="None",blank=True,null=True)   
    day=models.CharField(max_length=250,blank=True,null=True,default="")   
    money=models.PositiveSmallIntegerField(blank=True,null=True,default=0)   
    starting_time=models.CharField(max_length=250,default="",blank=True,null=True)  
    finishing_time=models.CharField(max_length=250,default="",blank=True,null=True)
    date=models.DateField(null=True)
    is_paid=models.CharField(max_length=50,default="no")
    meeting_method=models.CharField(max_length=50,default="ourSystem",blank=True,null=True)
    status=models.CharField(max_length=100,default="pending")
    

    class Meta:
        db_table="timeschedule"
        verbose_name ="müsait zaman"  
        verbose_name_plural ="müsait zamanlar"

    def __str__(self):
        return self.doctor.get_full_name()


    def is_upcoming(self):
        today=date.today()
        if(self.date<today):
            return True 
        else:
            return False


    
    # def get_day_name(self):
    #     a = calendar.day_name[self.date.weekday()]  
    #     return a

    
    # def get_date(self):
    #     day=getDayEnglish(self.day)
    #     my_date = datetime.date.today()
    #     a = calendar.day_name[self.date.weekday()]  
    #     weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    #     now = weekdays.index(a)
    #     later = weekdays.index(day)
    #     if later>=now:
    #         date = my_date - timedelta(days= now - later)
    #     else:
    #         date = my_date + timedelta(days= 6)
    #     return date

# class hakkimizdaModel(models.Model):
#     yazi=models.TextField(
#         blank=False,
#         null=False
#     )
#     created_date=models.DateTimeField(auto_now_add=True)
#     updated_date=models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table="Hakkimizda"
#         verbose_name = 'Hakkımızda Yazısı'
#         verbose_name_plural = 'Hakkımızda Yazısı'




class indexDoktorlarYaziModel(models.Model):
    yazi=RichTextField()
    top_title=models.CharField(
        max_length=250,
        blank=True,
        null=True
    )
    bottom_title=models.TextField(
        max_length=250,
        blank=True,
        null=True
    )   
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="İndex_Yazisi"
        verbose_name = 'İndex Yazısı'
        verbose_name_plural = 'İndex Yazısı'





class footerModel(models.Model):
    aciklamaYazisi=RichTextField()
    facebook=models.CharField(max_length=250,blank=True,null=True)   
    twitter=models.CharField(max_length=250,blank=True,null=True)   
    instagram=models.CharField(max_length=250,blank=True,null=True)   
    pinterest=models.CharField(max_length=250,blank=True,null=True)   
    linkedin=models.CharField(max_length=250,blank=True,null=True)   
    youtube=models.CharField(max_length=250,blank=True,null=True)    
    address=models.CharField(max_length=250,blank=True,null=True)    
    phone=models.CharField(max_length=250,blank=True,null=True)    
    email=models.EmailField(max_length=250,blank=True,null=True)    
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    class Meta:
        db_table="footer"
        verbose_name = 'Footer_Ayari'
        verbose_name_plural = 'Footer_Ayari'





class doctorFeatureIndexModel(models.Model):
    image=models.ImageField(upload_to="doktor_ozellik_image",blank=True,null=True)
    yazi=RichTextField()
    top_title=models.CharField(max_length=250,blank=True,null=True)   
    
    class Meta:
        db_table="doctorFeatureIndex"
        verbose_name = 'doctorFeatureIndex_Ayari'
        verbose_name_plural = 'doctorFeatureIndex_Ayari'

    



class featureModel(models.Model):
    image=models.ImageField(upload_to="doktor_ozellik_image/feature",blank=True,null=True)
    name=models.CharField(max_length=250,blank=True,null=True)   
    
    class Meta:
        db_table="feature"
        verbose_name = 'feature_model'
        verbose_name_plural = 'feature_model'






class logoModel(models.Model):
    anaLogo=models.ImageField(upload_to="logolar",blank=True,null=True)
    footerLogo=models.ImageField(upload_to="logolar",blank=True,null=True)
    
    class Meta:
        db_table="logolar"
        verbose_name = 'logo'
        verbose_name_plural = 'logolar'
    




class IletisimModel(models.Model):
    DURATION = (
        ("nobody" , "Lütfen kim olduğunuzu belirtiniz"),
        ("Ben bir doktorum ve sitenize üyeyim" , "Ben bir doktorum ve sitenize üyeyim"),
        ("Ben bir doktorum ancak sitenize üye değilim" , "Ben bir doktorum ancak sitenize üye değilim"),
        ("Hastayım/Ziyaretçiyim" , "Hastayım/Ziyaretçiyim"), 
        ("Medya ve İşbirliği" , "Medya ve İşbirliği"),
       
    )
    whoIs=models.CharField(choices=DURATION,default="None",max_length=150)   
    fullName=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)
    subject=models.CharField(max_length=100)
    mesaj=models.TextField()
    olusturulma_tarihi=models.DateTimeField(auto_now_add=True)
    okundu_bilgisi = models.CharField(
        default="okunmadı",
        max_length=30,
    )
    class Meta:
        db_table="iletisim"
        verbose_name = "İletişim"
        verbose_name_plural = "İletişim"

    def __str__(self):
        return self.email





class appointmentModel(models.Model): 
    doctor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="appointmentsOfDoctor")  
    patient=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,null=True,blank=True,related_name="appointmentsOfPatient")  
    duration=models.PositiveSmallIntegerField()   
    day=models.CharField(max_length=250)   
    money=models.PositiveSmallIntegerField()   
    starting_time=models.CharField(max_length=250)  
    finishing_time=models.CharField(max_length=250)
    meeting_method=models.CharField(max_length=50,default="ourSystem",blank=True,null=True)
    date=models.DateField()
    totalDuration=models.TimeField(blank=True,null=True)

    class Meta:
        db_table="appointments"
        verbose_name ="fatura"  
        verbose_name_plural ="faturalar"

    def __str__(self):
        return self.doctor.get_full_name()


    def is_upcoming(self):
        today=date.today()
        if(self.date<today):
            return True 
        else:
            return False





class deletedAppointmentModel(models.Model): 
    doctor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="deletedAppointmentsOfDoctor")  
    patient=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,null=True,blank=True,related_name="deleetdAppointmentsOfPatient")  
    duration=models.PositiveSmallIntegerField()   
    day=models.CharField(max_length=250)   
    money=models.PositiveSmallIntegerField()   
    starting_time=models.CharField(max_length=250)  
    finishing_time=models.CharField(max_length=250)
    meeting_method=models.CharField(max_length=50,default="ourSystem",blank=True,null=True)
    date=models.DateField()

    class Meta:
        db_table="deletedAppointments"
        verbose_name ="silinenFatura"  
        verbose_name_plural ="silinenFaturalar"

    def __str__(self):
        return self.doctor.get_full_name()


    def is_upcoming(self):
        today=date.today()
        if(self.date<today):
            return True 
        else:
            return False





class iletisimSettingsModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="iletisimSettings")  
    whatsapp=models.CharField(max_length=250,blank=True,null=True)   
    zoom=models.CharField(max_length=250,blank=True,null=True)   
    skype=models.CharField(max_length=250,blank=True,null=True)   
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="iletisimSettingsModel"
        verbose_name = 'iletisim_ayarlar_'
        verbose_name_plural = 'iletisim_ayarlari_'