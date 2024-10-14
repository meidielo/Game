from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255,blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)
    confirm_password = models.CharField(max_length=255,blank=True, null=True)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username if self.user else "No User"

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class ProfileManager(BaseUserManager):
#     def create_user(self, username, password=None):
#         if not username:
#             raise ValueError('Users must have a username')
#         user = self.model(username=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

# class Profile(AbstractBaseUser):
#     username = models.CharField(max_length=255, default='defaultusername', unique=True)
#     password = models.CharField(max_length=255, default='defaultpassword')
#     confirm_password = models.CharField(max_length=255, default='defaultpassword')
#     points = models.IntegerField(default=0)
    
#     objects = ProfileManager()

#     USERNAME_FIELD = 'username'

#     def __str__(self):
#         return self.username