from django.shortcuts import render
from . import models, forms

#Home Page
def home(request):
    banners=models.Banners.objects.all()
    services=models.Service.objects.all()[:3]
    return render(request, 'home.html', {'banners':banners, 'services':services})

#Page details
def page_details(request, id):
    page=models.Page.objects.get(id=id)
    return render (request, 'page.html', {'page':page})

#FAQ
def faq_list(request):
    faq=models.FAQ.objects.all()
    return render (request, 'faq.html', {'faqs':faq})

#Enquiry
def enquiry(request):
    msg = ''
    if request.method =='POST':
        form=forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            msg='Enquiry Submitted! We will get back to you as soon as possible'
    form=forms.EnquiryForm
    return render (request, 'enquiry.html', {'form':form, 'msg':msg})

#Gallery
def gallery(request):
    gallery=models.Gallery.objects.all().order_by('-id')
    return render (request, 'gallery.html', {'galleries':gallery})

#GalleryImage
def gallery_details(request, id):
    gallery=models.Gallery.objects.get(id=id)
    gallery_imgs=models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render (request, 'gallery_imgs.html', {'gallery_imgs':gallery_imgs, 'gallery':gallery})

#Sub Plans
def pricing(request):
    pricing=models.SubPlan.objects.all()
    dfeatures=models.SubPlanFeature.objects.distinct()
    return render(request, 'pricing.html', {'plans':pricing, 'dfeatures':dfeatures})