from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Banners Model
class Banners(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Services Model
class Service(models.Model):
    title=models.CharField(max_length=150)
    details=models.TextField()
    img = models.ImageField(upload_to="services/", null=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))

#Pages
class Page(models.Model):
    title=models.CharField(max_length=200)
    detail=models.TextField()

    def __str__(self):
        return self.title
    
#FAQ
class FAQ(models.Model):
    question=models.TextField()
    answer=models.TextField()

    def __str__(self):
        return self.question
    
#Enquiry Model
class Enquiry(models.Model):
    full_name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone_number=models.IntegerField()
    details=models.TextField()
    send_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name
    
#Gallery Model
class Gallery(models.Model):
    img=models.ImageField(upload_to='gallery/', null=True)
    title=models.CharField(max_length=150)
    details=models.TextField()

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))
    
#Gallery Images Model
class GalleryImage(models.Model):
    gallery=models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    img=models.ImageField(upload_to='gallery_imgs/', null=True)
    alt_text=models.CharField(max_length=150)

    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Subsription Plans
class SubPlan(models.Model):
    title=models.CharField(max_length=150)
    price=models.IntegerField()
    max_member=models.IntegerField(null=True)
    highlight_status=models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title

# Subscription Plans Features
class SubPlanFeature(models.Model):
    subplan=models.ManyToManyField(SubPlan)
    title=models.CharField(max_length=150)

    def __str__(self):
        return self.title
    
#Discount Package
class PlanDiscount(models.Model):
    subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
    total_month=models.IntegerField()
    total_discount = models.IntegerField()

    def __str__(self):
        return str (self.total_month)
    
#Subscriber
class Subscriber(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tel=models.CharField(max_length=20)
    address=models.TextField()
    img=models.ImageField(upload_to="subs/")

    def __str__(self):
        return str (self.user)

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" width="80" />' % (self.img.url))
        else:
            return "No_Image"
    
    @receiver(post_save, sender=User)
    def create_subscriber(sender, instance, created, **kwargs):
        if created:
            Subscriber.objects.create(user=instance)
    
    
#Subscription
class Subscription(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan=models.ForeignKey(SubPlan, on_delete=models.CASCADE, null=True)
    price=models.CharField(max_length=50)