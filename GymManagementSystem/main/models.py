from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

#Banners Model
class Banners(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural="Banners"

    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Services Model
class Service(models.Model):
    title=models.CharField(max_length=150)
    details=RichTextField()
    img = models.ImageField(upload_to="services/", null=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))

#Pages
class Page(models.Model):
    title=models.CharField(max_length=200)
    detail=RichTextField()

    def __str__(self):
        return self.title
    
#FAQ
class FAQ(models.Model):
    question=models.TextField()
    answer=RichTextField()

    def __str__(self):
        return self.question
    
#Enquiry Model
class Enquiry(models.Model):
    full_name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone_number=models.IntegerField()
    details=RichTextField()
    send_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Enquiries"

    def __str__(self) -> str:
        return self.full_name
    
#Gallery Model
class Gallery(models.Model):
    img=models.ImageField(upload_to='gallery/', null=True)
    title=models.CharField(max_length=150)
    details=RichTextField()

    class Meta:
        verbose_name_plural="Galleries"

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
    validity_period=models.IntegerField(null=True)

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
    sub_date=models.DateField(auto_now_add=True, null=True)

#Trainer
class Trainer(models.Model):
    Full_Name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    Email = models.EmailField()
    username = models.CharField(max_length=100, null=True)
    pwd = models.CharField(max_length=50, null=True)
    Home_Address = models.TextField()
    Is_active = models.BooleanField(default=False)
    details = RichTextField()
    profile_picture=models.ImageField(upload_to="Trainers/")
    salary=models.IntegerField(default=0)
    
    #Social Links
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    instagram = models.URLField(null=True)
    youtube = models.URLField(null=True)

    def __str__(self):
        return str (self.Full_Name)
    
    def image_tag(self):
        if self.profile_picture:
            return mark_safe('<img src="%s" width="60" />' % (self.profile_picture.url))
        else:
            return "No_Image"
        
#Subscriber Notification Model
class Notification(models.Model):
    notification_detail = RichTextField()
    read_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    read_by_Trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str (self.notification_detail)
    
#Notiification MarkAsRead
class NotifUserStatus(models.Model):
    notif=models.ForeignKey(Notification, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="User Notification Status"

#Assign Subscribers to Trainer Model
class SubsToTrainer(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainer= models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return str (self.user)
    
#Trainer's Achievements
class TrainersAchievements(models.Model):
    trainer= models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = RichTextField()
    img=models.ImageField(upload_to="Trainers_Acheievements/")

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" width="60" />' % (self.img.url))
        else:
            return "No_Image"
    
    def __str__(self):
        return str (self.title)
    
#Trainer Salary model
class TrainerSalary(models.Model):
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
    amount=models.IntegerField()
    amount_date=models.DateField()
    remarks=models.TextField(blank=True)

    class Meta:
        verbose_name_plural="Trainer's Salaries"

    def __str__(self):
        return str (self.trainer.Full_Name)
    
#Trainer Notification Model
class TrainerNotification(models.Model):
    notif_msg=RichTextField()

    def __str__(self):
        return str (self.notif_msg)
    
    def save(self, *args, **kwargs):
        super(TrainerNotification, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        notif = self.notif_msg
        total = TrainerNotification.objects.all().count()
        async_to_sync(channel_layer.group_send)(
            'noti_group_name',{
                'type':'send_notification',
                'value':json.dumps({'notif':notif, 'total':total})
            }
        )
    
#Notiification MarkAsRead By Trainer
class NotifTrainerStatus(models.Model):
    notif=models.ForeignKey(TrainerNotification, on_delete=models.CASCADE)
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Trainer Notification Status"

#Trainer messages Model
class TrainerMsg(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    message=RichTextField()

    class Meta:
        verbose_name_plural="Trainer Messages"

#Reports
class TrainerSubscriberReport(models.Model):
    report_a_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name='report_a_trainer')
    report_a_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='report_a_user')
    reporting_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, related_name='reporting_trainer')
    reporting_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reporting_user')
    report_msg = RichTextField()

class AppSettings(models.Model):
    app_logo = models.ImageField(upload_to='logo/')

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" />' % (self.app_logo.url))