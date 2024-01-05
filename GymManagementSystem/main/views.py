from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.db.models import Count
from datetime import timedelta
from .models import Page, Trainer
from .templatetags.check_package import check_plan_validity

#Home Page
def home(request):
    banners=models.Banners.objects.all()
    services=models.Service.objects.all()[:3]
    gimgs=models.GalleryImage.objects.all().order_by('-id') [:9]
    about_us_page = Page.objects.get(id=1)
    return render(request, 'home.html', {'banners':banners, 'services':services, 'gimgs':gimgs, 'about_us_page': about_us_page})

#Page details
def page_details(request, id):
    page=models.Page.objects.get(id=id)
    return render (request, 'page.html', {'page':page})

#Services Details
def service_details(request, id):
    service_details=models.Service.objects.get(id=id)
    return render (request, 'services.html', {'service_details':service_details})

#FAQ
def faq_list(request):
    faq=models.FAQ.objects.all()
    return render (request, 'faq.html', {'faqs':faq})

#Contact Page
def contact_us(request):
    return render (request, 'contact_us.html')

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
@login_required
def pricing(request):
    pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = models.SubPlanFeature.objects.all()

    countdown_values = {}

    # Check if the user is authenticated before querying for user-specific data
    if request.user.is_authenticated:
        for pric in pricing:
            check_validity = check_plan_validity(request.user.id, pric.id)
            if check_validity[0]:
                countdown_values[pric.id] = check_validity[1] * 86400000
    else:
        # If the user is not authenticated, set countdown_values to an empty dictionary
        countdown_values = {}

    return render(request, 'pricing.html', {'plans': pricing, 'dfeatures': dfeatures, 'countdown_values': countdown_values})

#Signup
def signup(request):
    msg = None
    form = forms.Signup()

    if request.method == 'POST':
        form = forms.Signup(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the login page upon successful signup
            return redirect('login')
        else:
            # Extract plain text error message from form errors
            error_message = ', '.join([' '.join(errors) for errors in form.errors.values()])
            msg = f'There was an error with the registration form: {error_message}'

    return render(request, 'registration/signup.html', {'form': form, 'msg': msg})




#Checkout View
def checkout(request, plan_id):
    PlanDetail=models.SubPlan.objects.get(pk=plan_id)
    return render(request, 'checkout.html', {'Plan':PlanDetail})

#Checkout session
stripe.api_key = 'sk_test_51KlzlxCxXy9cWFkINPAB3WbgMOW6hnNf4SCVFjb0OKutMxyh0EQHWgxtxx5vYu2vxHjDmItkJyhf5ROOxzvYASe900lw3jNHvX'
def checkout_session(request, plan_id):
    try:
        plan = models.SubPlan.objects.get(pk=plan_id)
        selected_discount_id = request.POST.get('selected_discount_id')

        # Retrieve the selected discount based on the selected_discount_id
        selected_discount = models.PlanDiscount.objects.get(pk=selected_discount_id)

        # Calculate the unit amount to be sent to Stripe
        unit_amount = int(plan.price * 100)  # Convert to cents

        # Apply the selected discount
        if selected_discount.total_discount > 0:
            unit_amount -= int((unit_amount * selected_discount.total_discount) / 100)

        # Multiply by the selected number of months
        selected_validity = int(request.POST.get('validity'))
        unit_amount *= selected_validity

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan.title,
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/payment_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/payment_cancel',
            client_reference_id=plan_id
        )

        return redirect(session.url, code=303)
    except Exception as e:
        # Handle exceptions appropriately
        return HttpResponseBadRequest("Error creating checkout session.")

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
    msg.content_subtype = "html"
    msg.send()
    return render(request, 'success.html')

#Payment_Cancel View
def payment_cancel(request):
    return render(request, 'cancel.html')

#User Dashboard View
def user_dashboard(request):
    try:
        current_plan=models.Subscription.objects.get(user=request.user)
        assigned_trainer=models.SubsToTrainer.objects.get(user=request.user)
        enddate=current_plan.sub_date+timedelta(days=current_plan.plan.validity_period)
    except models.SubsToTrainer.DoesNotExist:
        assigned_trainer = None
        enddate = None
    except models.Subscription.DoesNotExist:
        current_plan = None
        assigned_trainer = None
        enddate = None

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
    # Check if the trainer is logged in
    if 'trainerid' in request.session:
        trainer_id = request.session['trainerid']
        trainer = get_object_or_404(Trainer, id=trainer_id)
        return render(request, 'trainer/dashboard.html', {'trainer': trainer})
    else:
        # Handle the case where the trainer is not logged in
        return redirect('trainerlogin')

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

from django.shortcuts import redirect

# Report For User
def report_a_trainer(request):
    user = request.user
    msg = ''

    if request.method == 'POST':
        form = forms.ReportATrainerForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.reporting_user = user
            new_form.save()
            msg = 'Report submitted and will be treated with urgency!'
        else:
            msg = 'Invalid!!!'
    else:
        # Instantiate the form with the initial value for report_from_user
        form = forms.ReportATrainerForm(initial={'reporting_user': user.id})

    return render(request, 'report_a_trainer.html', {'form': form, 'msg': msg})

# Report For User
def report_a_user(request):
    trainer = models.Trainer.objects.get(id=request.session.get('trainerid'))
    msg = ''

    if request.method == 'POST':
        form = forms.ReportAUserForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.reporting_trainer = trainer
            new_form.save()
            msg = 'Report submitted and will be treated with urgency!'
        else:
            msg = 'Invalid!!!'
    else:
        # Instantiate the form with the initial value for report_from_trainer
        form = forms.ReportAUserForm(initial={'reporting_trainer': trainer.id})

    return render(request, 'report_a_user.html', {'form': form, 'msg': msg})
