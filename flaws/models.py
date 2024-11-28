from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    session_token = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.username

# FIX for flaw XX
#from django.contrib.auth.models import AbstractUser
#
#class User(AbstractUser):
#    username = models.CharField(max_length=20, unique=True)

#or
#
#class User(models.Model):
#    username = models.CharField(max_length=20, unique=True)
#
#    def set_password(self, raw_password):
#        #Hash the password before saving it.
#        self.password = make_password(raw_password)
#
#    def check_password(self, raw_password):
#        #Check if the provided password matches the hashed one.
#        from django.contrib.auth.hashers import check_password
#        return check_password(raw_password, self.password)
#
#    def __str__(self):
#        return self.username

class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Age: {self.age})"