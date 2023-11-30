from django.db import models
from django.utils.html import mark_safe

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
    phone_number=models.CharField(max_length=15)
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