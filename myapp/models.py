from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# umumiy list
class GeneralList(models.Model):
    service=models.CharField(max_length=200)
    firstname=models.CharField(max_length=20,null=True, blank=True)
    lastname=models.CharField(max_length=20,null=True, blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    user_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.service

# bajarilganlar
class CompletedList(models.Model):
    service=models.CharField(max_length=200)
    firstname=models.CharField(max_length=20,null=True, blank=True)
    lastname=models.CharField(max_length=20,null=True, blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    user_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    ofis_user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.service

# bekor qilinganlar
class CancelledList(models.Model):
    service=models.CharField(max_length=200)
    firstname=models.CharField(max_length=20,null=True, blank=True)
    lastname=models.CharField(max_length=20,null=True, blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    user_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    ofis_user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.service

# kelmaganlar
class NotComeList(models.Model):
    service=models.CharField(max_length=200)
    firstname=models.CharField(max_length=20,null=True, blank=True)
    lastname=models.CharField(max_length=20,null=True, blank=True)
    phone=models.CharField(max_length=13,null=True, blank=True)
    user_telegram_id = models.CharField(max_length=15, null=True, blank=True)
    ofis_user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.service