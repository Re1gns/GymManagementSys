from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home, name='home'),
    path('pagedetail/<int:id>',views.page_details, name='pagedetail'),
    path('faq', views.faq_list, name='faq'),
    path('enquiry', views.enquiry, name='enquiry'),
    path('gallery', views.gallery, name='gallery'),
    path('gallery_details/<int:id>', views.gallery_details, name='gallery_details'),
    path('pricing', views.pricing, name='pricing'),
    path('accounts/signup', views.signup, name='signup'),
    path('checkout/<int:plan_id>', views.checkout, name='checkout'),
    path('checkout_session/<int:plan_id>', views.checkout_session, name='checkout_session'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_cancel', views.payment_cancel, name='payment_cancel'),
    path('user/dashboard', views.user_dashboard, name='user_dashboard'),
    path('user/edit_profile', views.edit_profile, name='update_profile'),
    path('trainerlogin', views.trainerlogin, name='trainerlogin'),
    path('trainerlogout', views.trainerlogout, name='trainerlogout'),
    path('notification', views.notification, name='notification'),
    path('get_notification', views.get_notification, name='get_notification'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )