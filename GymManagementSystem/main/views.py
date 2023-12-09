from django.shortcuts import render, redirect
from . import models, forms
import stripe

#Home Page
def home(request):
    banners=models.Banners.objects.all()
    services=models.Service.objects.all()[:3]
    gimgs=models.GalleryImage.objects.all().order_by('-id') [:9]
    return render(request, 'home.html', {'banners':banners, 'services':services, 'gimgs':gimgs})

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
    pricing=models.SubPlan.objects.all().order_by('price')
    dfeatures=models.SubPlanFeature.objects.all()
    return render(request, 'pricing.html', {'plans':pricing, 'dfeatures':dfeatures})

#Signup
def signup(request):
    msg=None
    if request.method =='POST':
        form=forms.Signup(request.POST)
        if form.is_valid():
            form.save()
            msg='Thank you for registering'
    form=forms.Signup
    return render(request, 'registration/signup.html', {'form':form, 'msg':msg})

#Checkout View
def checkout(request, plan_id):
    PlanDetail=models.SubPlan.objects.get(pk=plan_id)
    return render(request, 'checkout.html', {'Plan':PlanDetail})

#Checkout session
stripe.api_key = ''
def checkout_session(request, plan_id):
    plan=models.SubPlan.objects.get(pk=plan_id)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data':{
                'currency':'usd',
                'product_data':{
                    'name':plan.title,
                },
                'unit_amount':plan.price*100
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success',
        cancel_url='http://127.0.0.1:8000/payment_cancel',
)
    return redirect(session.url, code=303)

#Payment_Success
def payment_success(request):
    return render(request, 'success.html')

#Payment_Cancel
def payment_cancel(request):
    return render(request, 'cancel.html')