from django.shortcuts import render, redirect
from . import models, forms
import stripe
from django.core import serializers
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import get_template

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
stripe.api_key = 'sk_test_51KlzlxCxXy9cWFkINPAB3WbgMOW6hnNf4SCVFjb0OKutMxyh0EQHWgxtxx5vYu2vxHjDmItkJyhf5ROOxzvYASe900lw3jNHvX'
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
        success_url='http://127.0.0.1:8000/payment_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/payment_cancel',
        client_reference_id=plan_id
)
    return redirect(session.url, code=303)

#Payment_Success
def payment_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = models.SubPlan.objects.get(pk=plan_id)
    user = request.user
    models.Subscription.objects.create(
        plan = plan,
        user = user,
        price = plan.price
    )
    subject = 'Order Confirmation'
    html_content = get_template('orderemail.html').render({'title':plan.title})
    from_email = 'lreigns12@gmail.com'
    msg = EmailMessage(subject, html_content, from_email, ['vic@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return render(request, 'success.html')

#Payment_Cancel View
def payment_cancel(request):
    return render(request, 'cancel.html')

#User Dashboard View
def user_dashboard(request):
    return render(request, 'user/dashboard.html')

#Edit Profile View
def edit_profile(request):
    msg=None
    if request.method == 'POST':
        form = forms.EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg="Profile Updated Successfully"
    form = forms.EditProfile(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form':form, 'msg':msg})

#Trainer Login View
def trainerlogin(request):
    msg = ''
    if request.method=='POST':
        username=request.POST['username']
        pwd=request.POST['pwd']
        trainer=models.Trainer.objects.filter(username=username, pwd=pwd).count()
        if trainer > 0:
            request.session['trainerLogin'] = True
            return redirect('/trainer_dashboard')
        else:
            msg='Invalid'
    form=forms.TrainerLogin
    return render(request, 'trainer/login.html', {'form':form, 'msg':msg})

#Trainer Login View
def trainerlogout(request):
    del request.session['trainerLogin']
    return redirect('/trainerlogin')

#Notification View
def notification(request):
    data = models.Notification.objects.all().order_by('-id')
    return render(request, 'notification.html', {'data':data})

#Get Notifications View
def get_notification(request):
    data = models.Notification.objects.all().order_by('-id')
    jsonData = serializers.serialize('json', data)
    return JsonResponse({'data':jsonData})
    