from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField
import uuid
# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50,blank=True)
    profimag=models.ImageField(upload_to='profimages',default='default.png')
    phoneno=models.CharField(max_length=11,null=True,blank=True)
    otp=models.IntegerField(null=True,blank=True)
    uid=models.UUIDField(default=uuid.uuid4)
    address=models.TextField(blank=True)
    def __str__(self):
        return self.name

class posts(models.Model):
    post_user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post_id=models.UUIDField(default=uuid.uuid4)
    crop=models.CharField(max_length=20,null=True)
    price=models.CharField(max_length=20,null=True)
    address=models.TextField(blank=True)
    icon=models.CharField(max_length=2,blank=True)
    def __str__(self):
        return self.post_user.user.username

class Schemes(models.Model):
    id=models.IntegerField(primary_key=True)
    s_name=models.CharField(max_length=100)
    img=models.ImageField(upload_to='Schemeimg')
    state=models.TextField()
    link=models.URLField(blank=True)
    pdf=models.URLField(blank=True)
    hindi_pdf=models.URLField(blank=True)
    video=EmbedVideoField(blank=True)
    desc=models.TextField(blank=True)
    duration=models.TextField(blank=True)

    def __str__(self):
        return self.s_name

class chats(models.Model):
    messages=models.TextField()
    response=models.TextField()
    curr_user=models.CharField(max_length=100)

class crophealth(models.Model):
    name=models.TextField()
    growth_stage=models.TextField()
    condition=models.TextField()
    issues=models.TextField()
    user=models.CharField(max_length=100)

class loan(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to="loan")
    purpose=models.TextField()
    eligibility=models.TextField()

    def __str__(self):
        return self.name

    
    
    