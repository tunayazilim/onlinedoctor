from django.db import models

# Create your models here.




class PageModel(models.Model):
    meta_title=models.CharField(max_length=500,blank=True,null=True) 
    meta_description=models.CharField(max_length=500,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=500,blank=True,null=True)    
    view_name=models.CharField(max_length=100,blank=True,null=True)    
    
    class Meta:
        db_table="pageModel"
        verbose_name ="Sayfa Modeli"  
        verbose_name_plural ="Sayfa Modelleri"

    def __str__(self):
        return self.meta_title







class topMenuModel(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)   
    url=models.CharField(max_length=150,blank=True,null=True)   
    userType=models.CharField(max_length=100,blank=True,null=True)   
    menuType=models.CharField(max_length=100,blank=True,null=True,default="Üst Menü")   
    menuSira=models.SmallIntegerField(default=0)


    class Meta:
        db_table="topMenuModel"
        verbose_name ="Üst Menü"  
        verbose_name_plural ="Üst Menüler"

    def __str__(self):
        return self.name


    def get_bottom_menuler(self):
        return bottomMenuModel.objects.filter(topMenu=self).order_by("menuSira")
    

    def has_bottom_menu(self):
        menuler=bottomMenuModel.objects.filter(topMenu=self).all()
        if menuler.count()>0:
            return True
        else:
            return False



class bottomMenuModel(models.Model):
    topMenu=models.ForeignKey(topMenuModel,on_delete=models.CASCADE,related_name="bottomMenus")  
    name=models.CharField(max_length=100,blank=True,null=True)   
    url=models.CharField(max_length=150,blank=True,null=True)   
    userType=models.CharField(max_length=100,blank=True,null=True)   
    menuType=models.CharField(max_length=100,blank=True,null=True,default="Alt Menü") 
    menuSira=models.SmallIntegerField(default=0)


    class Meta:
        db_table="bottomMenuModel"
        verbose_name ="Alt Menü"  
        verbose_name_plural ="Alt Menüler"

    def __str__(self):
        return self.name


