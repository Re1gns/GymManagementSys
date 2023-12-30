from django.shortcuts import render, redirect
from . import models, forms
import stripe
from django.core import serializers
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.db.models import Count
from datetime import timedelta

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
    pricing=models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
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
    current_plan=models.Subscription.objects.get(user=request.user)
    assigned_trainer=models.SubsToTrainer.objects.get(user=request.user)
    enddate=current_plan.sub_date+timedelta(days=current_plan.plan.validity_period)

    #Notifications
    data = models.Notification.objects.all().order_by('-id')
    notifStatus=False
    jsonData=[]
    TotalUnread=0
    for d in data:
        try:
            notifStatusData=models.NotifUserStatus.objects.get(user=request.user, notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            TotalUnread+=1
    return render(request, 'user/dashboard.html', {'current_plan':current_plan, 'assigned_trainer':assigned_trainer, 'TotalUnread':TotalUnread, 'enddate':enddate})

#Change Password view

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
            trainer=models.Trainer.objects.filter(username=username, pwd=pwd).first()
            request.session['trainerLogin'] = True
            request.session['trainerid'] = trainer.id
            msg='success'
            return redirect('/trainer_dashboard')
        else:
            msg='Invalid'
    form=forms.TrainerLogin
    return render(request, 'trainer/login.html', {'form':form, 'msg':msg})

#Trainer Logout View
def trainerlogout(request):
    del request.session['trainerLogin']
    return redirect('/trainerlogin')

#Trainer Dashboard
def trainer_dashboard(request):
    return render(request, 'trainer/dashboard.html')

#Trainer Profile Update
def trainer_profile(request):
    trainer_id=request.session['trainerid']
    trainer=models.Trainer.objects.get(id=trainer_id)
    msg=None
    if request.method == 'POST':
        form=forms.TrainerProfile(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            msg='Profile updated successfully!'
    form=forms.TrainerProfile(instance=trainer)
    return render(request, 'trainer/profile.html', {'form':form, 'msg':msg})

#Notification View
def notification(request):
    data = models.Notification.objects.all().order_by('-id')
    return render(request, 'notification.html', {'data':data})

#Get Notifications View
def get_notification(request):
    data = models.Notification.objects.all().order_by('-id')
    notifStatus=False
    jsonData=[]
    TotalUnread=0
    for d in data:
        try:
            notifStatusData=models.NotifUserStatus.objects.get(user=request.user, notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            TotalUnread+=1
        jsonData.append({
                'pk':d.id,
                'notification_detail':d.notification_detail,
                'notifStatus':notifStatus
            })
    #jsonData = serializers.serialize('json', data)
    return JsonResponse({'data':jsonData, 'TotalUnread':TotalUnread})

#User Notifications_Mark_as Read View
def mark_read_notification(request):
    notif=request.GET['notif']
    notif=models.Notification.objects.get(pk=notif)
    user=request.user
    models.NotifUserStatus.objects.create(notif=notif, user=user, status=True)
    return JsonResponse({'bool':True})

#Assigned Subscribers View
def assigned_subscribers(request):
    trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
    assigned_subs=models.SubsToTrainer.objects.filter(trainer=trainer).order_by('-id')
    return render(request, 'trainer/assigned_subs.html', {'assigned_subs':assigned_subs})

#Trainer's Salary View
def trainer_salary(request):
    trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
    trainer_salaries=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
    return render(request, 'trainer/salary.html', {'trainer_salaries':trainer_salaries})

#Trainer Change Password
def trainer_changepassword(request):
    msg=None
    if request.method=='POST':
        new_password=request.POST['new_password']
        updateRes=models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_password)
        if updateRes:
            del request.session['trainerLogin']
            return redirect('/trainerlogin')
        else:
            msg='Something went wrong!!!'
    form=forms.TrainerChangePassword
    return render(request, 'trainer/trainer_changepassword.html', {'form':form, 'msg':msg})

#Trainer's Notification View
def trainer_notification(request):
    data = models.TrainerNotification.objects.all().order_by('-id')
    trainer = models.Trainer.objects.get(id=request.session['trainerid'])
    jsonData=[]
    TotalUnread = 0
    for d in data:
        try:
            notifStatusData=models.NotifTrainerStatus.objects.get(trainer=trainer, notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            TotalUnread+=1
        jsonData.append({
                'pk':d.id,
                'notification_detail':d.notif_msg,
                'notifStatus':notifStatus
            })

    return render(request, 'trainer/notification.html', {'notification':jsonData, 'TotalUnread':TotalUnread})

#Trainer's Notifications_Mark_as Read View
def mark_read_trainer_notification(request):
    notif=request.GET['notif']
    notif=models.TrainerNotification.objects.get(pk=notif)
    trainer = models.Trainer.objects.get(id=request.session['trainerid'])
    models.NotifTrainerStatus.objects.create(notif=notif, trainer=trainer, status=True)

# Count Unread
    TotalUnread = 0
    data = models.TrainerNotification.objects.all().order_by('-id')
    for d in data:
        try:
            notifStatusData=models.NotifTrainerStatus.objects.get(trainer=trainer, notif=d)
            if notifStatusData:
                notifStatus=True
        except models.NotifTrainerStatus.DoesNotExist:
            notifStatus=False
        if not notifStatus:
            TotalUnread+=1

    return JsonResponse({'bool':True, 'TotalUnread':TotalUnread})

#Trainer messages View
def trainer_msgs(request):
    data = models.TrainerMsg.objects.all().order_by('-id')
    return render(request, 'trainer/messages.html', {'messages':data})