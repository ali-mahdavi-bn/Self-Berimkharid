from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from accounts.managers import UserManager


# from product.models import Upload


# Create your models here.
class User(AbstractBaseUser):
    userName = models.CharField(
        null=False,
        db_index=True,
        blank=True,
        max_length=200, unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phoneNumber = models.CharField(max_length=11)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    isAdmin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['email', 'firstName', 'lastName', 'phoneNumber']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        if self.type == 'superAdmin':
            return True
        return False


class VerifyUser(models.Model):
    phoneNumber = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    isUsed = models.BooleanField(default=False)
    mode = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class UserDetails(models.Model):
    pictureId = models.ForeignKey('upload.Upload', on_delete=models.CASCADE, null=True,
                                  related_name='Upload_UserDetails')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userId_UserDetails')
    gender = models.CharField(max_length=100, null=True, blank=True)
    nationalCode = models.CharField(max_length=100, null=True, blank=True)
    birth = models.DateTimeField(null=True, blank=True)
    lastLogin = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
