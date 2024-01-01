from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns=[
    #General Urls
    path('',views.home, name='home'),
    path('pagedetail/<int:id>',views.page_details, name='pagedetail'),
    path('servicedetail/<int:id>',views.service_details, name='servicedetail'),
    path('faq', views.faq_list, name='faq'),
    path('enquiry', views.enquiry, name='enquiry'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('gallery', views.gallery, name='gallery'),
    path('gallery_details/<int:id>', views.gallery_details, name='gallery_details'),

    #User Urls
    path('pricing', views.pricing, name='pricing'),
    path('accounts/signup', views.signup, name='signup'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html', success_url='/password_change_done/'), name='change_password'),
    path('checkout/<int:plan_id>', views.checkout, name='checkout'),
    path('checkout_session/<int:plan_id>', views.checkout_session, name='checkout_session'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_cancel', views.payment_cancel, name='payment_cancel'),
    path('user/dashboard', views.user_dashboard, name='user_dashboard'),
    path('user/edit_profile', views.edit_profile, name='update_profile'),

    #Trainer Urls
    path('trainerlogin', views.trainerlogin, name='trainerlogin'),
    path('trainerlogout', views.trainerlogout, name='trainerlogout'),
    path('trainer_dashboard', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer_profile', views.trainer_profile, name='trainer_profile'),
    path('assigned_subscribers', views.assigned_subscribers, name='assigned_subscribers'),
    path('trainer_salary', views.trainer_salary, name='trainer_salary'),
    path('trainer_changepassword', views.trainer_changepassword, name='trainer_changepassword'),
    path('trainer_notification', views.trainer_notification, name='trainer_notification'),
    path('mark_read_trainer_notification', views.mark_read_trainer_notification, name='mark_read_trainer_notification'),

    #Notification Urls
    path('notification', views.notification, name='notification'),
    path('get_notification', views.get_notification, name='get_notification'),
    path('mark_read_notification', views.mark_read_notification, name='mark_read_notification'),

    #Messages Urls
    path('messages', views.trainer_msgs, name='messages'),
    path('report_a_user', views.report_a_user, name='report_a_user'),
    path('report_a_trainer', views.report_a_trainer, name='report_a_trainer'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )