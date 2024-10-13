from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=255,blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)
    confirm_password = models.CharField(max_length=255,blank=True, null=True)
    # points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username