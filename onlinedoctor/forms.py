from os import name
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db.models.fields.files import ImageField
from django.forms.widgets import EmailInput, FileInput, PasswordInput, Select
from .models import CommentModel, CustomUserModel, IletisimModel, TimeScheduleModel, alanModel, alanYazilarModel, bannerModel, doctorFeatureIndexModel, featureModel, footerModel, iletisimSettingsModel, indexDoktorlarYaziModel, logoModel, socialMediaDoctorModel
from django.forms import ModelForm,TextInput,Textarea
from django import forms
from django_starfield import Stars
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class registerForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","email","phone_number","password1","password2","file","kimlik")
        widgets = {
            "first_name" : TextInput(attrs={"class":"form-control floating","type":"text","name":"first_name","required":""}),
            "last_name" : TextInput(attrs={"class":"form-control floating","name":"last_name","required":""}),
            "email" : EmailInput(attrs={"class":"form-control floating","type":"email","name":"email","required":""}),
            "phone_number" : TextInput(attrs={"class":"form-control floating","type":"tel","id":"phone","name":"phone_number","required":""}), 
            "file" : FileInput(attrs={"class":"form-control floating","type":"file","name":"file","required":""}),     
            "kimlik" : FileInput(attrs={"class":"form-control floating","type":"file","name":"kimlik","required":""}),           
            "password1" : PasswordInput(attrs={"class":"form-control floating","type":"password","name":"password1","required":""}),
            "password2" : PasswordInput(attrs={"class":"form-control floating","type":"password","name":"password2","required":""}),
            
        }
        labels={
            "file":"Diploma(max 10 mb)",
            "kimlik":"Kimlik(max 10 mb)"
        }
        


class DoctorBasicForm(UserChangeForm):    #kulllanılmadı
    password=None
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","username","email","phone_number","gender","date_of_birth","image")      
        CHOICES= (
            ('ERKEK', 'ERKEK'),
            ('KADIN', 'KADIN'))
        widgets = {
            "first_name" : TextInput(attrs={"class":"form-control"}),
            "last_name" : TextInput(attrs={"class":"form-control"}),
            "email" : EmailInput(attrs={"class":"form-control","type":"email"}),
            "phone_number" : TextInput(attrs={"class":"form-control"}),
            "username" : TextInput(attrs={"class":"form-control"}),
            "gender" : TextInput(attrs={"class":"form-control"}),
            "date_of_birth" : TextInput(attrs={"class":"form-control"}),            
            "image" : FileInput(attrs={"class":"form-control"})            
        }





class socialMediaDoctorForm(forms.ModelForm):
    class Meta:
        model = socialMediaDoctorModel
        exclude=("user",)
        widgets = {
            "facebook" : TextInput(attrs={"class":"form-control"}),
            "twitter" : TextInput(attrs={"class":"form-control"}),
            "instagram" : TextInput(attrs={"class":"form-control"}),
            "pinterest" : TextInput(attrs={"class":"form-control"}),
            "linkedin" : TextInput(attrs={"class":"form-control"}),
            "youtube" : TextInput(attrs={"class":"form-control"}),
          
        }
        # labels = {         
        #     'title': "Başlık",
        #     'kategoriler': "Kategoriler (Birden fazla kategori seçimi için CTRL tuşunu kullanabilirsiniz)",
        # }



class PatientBasicForm(UserChangeForm):    #kulllanılmadı
    password=None
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","date_of_birth","blood_group","email","phone_number","gender","city","state","address") 
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
        CHOICES= (
            ('Erkek', 'Erkek'),
            ('Kadın', 'Kadın'))
        gender = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control select"}), choices=CHOICES) 
        blood_group = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control select"}), choices=STATUS_BLOOD) 
       
        widgets = {
            #"image" : FileInput(attrs={"class":"form-control"}),        
            "first_name" : TextInput(attrs={"class":"form-control","required":""}),
            "last_name" : TextInput(attrs={"class":"form-control","required":""}),
            "date_of_birth" : TextInput(attrs={"class":"form-control floating","type":"date","required":""}),    
            "blood_group" : Select(attrs={"class":"form-control select","required":""}),
            "email" : EmailInput(attrs={"class":"form-control","type":"email","required":""}),
            "phone_number" : TextInput(attrs={"class":"form-control floating","type":"tel","id":"phone","name":"phone_number","required":""}),
            "gender" : Select(attrs={"class":"form-control select","required":""}),
            "city" : TextInput(attrs={"class":"form-control","required":""}),
            "state" : TextInput(attrs={"class":"form-control","required":""}),
            "address" : TextInput(attrs={"class":"form-control","required":""}),
             
        }
        labels = {         
            'date_of_birth': "Doğum Tarihi",
            'phone_number': "Telefon Numarası",
            'gender': "Cinsiyet",
            'city': "İl",
            'state': "İlçe",
            'address': "Adres"
        }




class CommentModelForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields=("star","comment")
        widgets = {           
            "star" : Stars(attrs={"class":"active fa fa-star"}),   
            "comment" : Textarea(attrs={"class":"form-control"}),          
        }




class TimeScheduleModelForm(forms.ModelForm):
    class Meta:
        model = TimeScheduleModel
        exclude=("doctor","starting_time","finishing_time")
        widgets = {           
            "duration" : Select(attrs={"class":"form-control select"}),   
            "day" : TextInput(attrs={"class":"form-control"}),    
            # "starting_time" : TextInput(attrs={"class":"form-control","type":"time"}),    
            # "finishing_time" : TextInput(attrs={"class":"form-control","type":"time"}),    

        }







class AlanModelForm(forms.ModelForm):
    class Meta:
        model = alanModel
        fields=("name","image")
        widgets = {           
            "name" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "image" : FileInput(attrs={"class":"form-control","type":"file"}),   

        }






class BannerModelForm(forms.ModelForm):
    class Meta:
        model = bannerModel
        fields=("top_title","bottom_title")
        widgets = {           
            "top_title" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "bottom_title" : TextInput(attrs={"class":"form-control","type":"text"}),   

        }





class AlanYazıModelForm(forms.ModelForm):
    class Meta:
        model = alanYazilarModel
        fields=("top_title","bottom_title")
        widgets = {           
            "top_title" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "bottom_title" : TextInput(attrs={"class":"form-control","type":"text"}),   

        }



class indexDoktorYaziModelForm(forms.ModelForm):
    class Meta:
        model = indexDoktorlarYaziModel
        fields=("top_title","bottom_title","yazi")
        widgets = {           
            "top_title" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "bottom_title" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "yazi" : Textarea(attrs={"class":"form-control"}),   
        }







class footerModelForm(forms.ModelForm):
    class Meta:
        model = footerModel
        exclude=("created_date","updated_date")
        widgets = {
            "footerLogo" : FileInput(attrs={"class":"form-control","type":"file"}),   
            "aciklamaYazisi" : Textarea(attrs={"class":"form-control"}),   
            "facebook" : TextInput(attrs={"class":"form-control"}),
            "twitter" : TextInput(attrs={"class":"form-control"}),
            "instagram" : TextInput(attrs={"class":"form-control"}),
            "pinterest" : TextInput(attrs={"class":"form-control"}),
            "linkedin" : TextInput(attrs={"class":"form-control"}),
            "youtube" : TextInput(attrs={"class":"form-control"}),
            "address" : TextInput(attrs={"class":"form-control"}),
            "phone" : TextInput(attrs={"class":"form-control"}),
            "email" : EmailInput(attrs={"class":"form-control"}),
          
        }
        # labels = {         
        #     'title': "Başlık",
        #     'kategoriler': "Kategoriler (Birden fazla kategori seçimi için CTRL tuşunu kullanabilirsiniz)",
        # }




class doctorFeatureIndexModelForm(forms.ModelForm):
    class Meta:
        model = doctorFeatureIndexModel
        fields=("image","top_title","yazi")
        widgets = {           
            "image" : FileInput(attrs={"class":"form-control","type":"file"}),   
            "top_title" : TextInput(attrs={"class":"form-control","type":"text"}),   
            "yazi" : Textarea(attrs={"class":"form-control"}),   
        }





class FeatureModelForm(forms.ModelForm):
    class Meta:
        model = featureModel
        fields=("image","name")
        widgets = {           
            "image" : FileInput(attrs={"class":"form-control","type":"file"}),   
            "name" : TextInput(attrs={"class":"form-control","type":"text"}),   
        }




class logoModelForm(forms.ModelForm):
    class Meta:
        model = logoModel
        fields=("__all__")
        widgets = {           
            "anaLogo" : FileInput(attrs={"class":"form-control","type":"file"}),   
            "footerLogo" : FileInput(attrs={"class":"form-control","type":"file"}),   

        }



class iletişimModelForm(forms.ModelForm):
    class Meta:
        model = IletisimModel
        exclude=("olusturulma_tarihi","okundu_bilgisi")
        widgets = {
            "whoIs" : Select(attrs={"style":"text-transform: none;","class":"form-control select","required":""}),
            "subject" : TextInput(attrs={"style":"text-transform: none;","class":"form-control","type":"text","required":"","placeholder":"Konu"}),
            "fullName" : TextInput(attrs={"style":"text-transform: none;","class":"form-control","type":"text","required":"","placeholder":"İsim Soyisim"}),
            "email" : TextInput(attrs={"style":"text-transform: none;","class":"form-control","type":"email","required":"","placeholder":"Email"}),  
            "mesaj" : Textarea(attrs={"style":"text-transform: none;","required":"","class":"form-control","rows":"5","placeholder":"Mesaj"}),
      
        }
        labels = {
            'whoIs': "Kim olduğunuzu belirtiniz",
            'subject': "Konu",
            'fullName': "İsim Soyisim",
            'email': "Email",
            'mesaj': "Mesaj"
        }




class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()





class iletisimSettingsModelForm(forms.ModelForm):
    class Meta:
        model = iletisimSettingsModel
        exclude=("user","created_date","updated_date")
        widgets = {
            "whatsapp" : TextInput(attrs={"class":"form-control"}),
            "zoom" : TextInput(attrs={"class":"form-control"}),
            "skype" : TextInput(attrs={"class":"form-control"}),
        }
        # labels = {         
        #     'title': "Başlık",
        #     'kategoriler': "Kategoriler (Birden fazla kategori seçimi için CTRL tuşunu kullanabilirsiniz)",
        # }