
from onlinedoctor.models import CustomUserModel




class EmailAuthBackend(object):
    def authenticate(self,request,username=None,password=None):
        try:
            user=CustomUserModel.objects.get(email=username) 
            if user.check_password(password):
                return user
            return None
        except CustomUserModel.DoesNotExist:
            return None
        

    
    def get_user(self,user_id):
        try:
            return CustomUserModel.objects.get(pk=user_id)
        except CustomUserModel.DoesNotExist:
            return None
        



