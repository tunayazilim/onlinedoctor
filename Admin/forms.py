from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import DateInput, DateTimeInput, EmailInput, FileInput, TextInput, Textarea
from Admin.models import PageModel, topMenuModel
from onlinedoctor.models import CustomUserModel





class PageModelForm(forms.ModelForm):
    class Meta:
        model = PageModel
        fields=("__all__")
        widgets = {
            "meta_title" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_title"}),
            "meta_description" : Textarea(attrs={"class":"form-control","type":"text","name":"meta_description","rows":"5","cols":"5"}),
            "meta_keywords" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_keywords"}),
            "view_name" : TextInput(attrs={"class":"form-control","type":"text","name":"view_name"}),           
        }
        




class ProfileAdminForm(UserChangeForm):    #kulllanılmadı
    password=None
    class Meta:
        model = CustomUserModel
        fields=("image","first_name","last_name","address","email","phone_number","city","date_of_birth","state","country")      
        widgets = {
            "image" : FileInput(attrs={"class":"form-control","type":"file"}),
            "first_name" : TextInput(attrs={"class":"form-control"}),
            "last_name" : TextInput(attrs={"class":"form-control"}),
            "date_of_birth" : TextInput(attrs={"class":"form-control","type":"date"}), 
            "email" : EmailInput(attrs={"class":"form-control","type":"email"}),
            "phone_number" : TextInput(attrs={"class":"form-control","type":"tel","id":"phone","name":"phone_number"}),
            "address" : TextInput(attrs={"class":"form-control"}),
            "city" : TextInput(attrs={"class":"form-control"}),                     
            "state" : TextInput(attrs={"class":"form-control"}),    
            "country" : TextInput(attrs={"class":"form-control"})         
        }
      



