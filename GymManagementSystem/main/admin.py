from django.contrib import admin
from . import models
from ckeditor.widgets import CKEditorWidget

class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')
admin.site.register(models.Banners, BannerAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(models.Service, ServiceAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display=('title',)
admin.site.register(models.Page, PageAdmin)

class FAQAdmin(admin.ModelAdmin):
    list_display=('question',)
admin.site.register(models.FAQ, FAQAdmin)

class EnquiryAdmin(admin.ModelAdmin):
    list_display=('full_name', 'email', 'phone_number', 'details', 'send_time')
admin.site.register(models.Enquiry, EnquiryAdmin)

class GalleryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(models.Gallery, GalleryAdmin)

class GalleryImageAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')
admin.site.register(models.GalleryImage, GalleryImageAdmin)

class SubPlanAdmin(admin.ModelAdmin):
    list_editable=('highlight_status', 'max_member',)
    list_display=('title', 'price', 'validity_period', 'max_member', 'highlight_status')
admin.site.register(models.SubPlan, SubPlanAdmin)

class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display=('title', 'subplans',)
    def subplans(self, obj):
        return " || ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature, SubPlanFeatureAdmin)

class PlanDiscountAdmin(admin.ModelAdmin):
    list_display=('subplan', 'total_month', 'total_discount')
admin.site.register(models.PlanDiscount, PlanDiscountAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    list_display=('user', 'image_tag', 'tel')
admin.site.register(models.Subscriber, SubscriberAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('user', 'plan', 'sub_date', 'price')
admin.site.register(models.Subscription, SubscriptionAdmin)

class TrainerAdmin(admin.ModelAdmin):
    list_editable = ('Is_active',)
    list_display=('Full_Name', 'Is_active', 'salary', 'tel', 'image_tag')
admin.site.register(models.Trainer, TrainerAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display=('notification_detail',)
admin.site.register(models.Notification, NotificationAdmin)

class NotifUserStatusAdmin(admin.ModelAdmin):
    list_display=('notif', 'user', 'status')
admin.site.register(models.NotifUserStatus, NotifUserStatusAdmin)

class SubsToTrainerAdmin(admin.ModelAdmin):
    list_display=('user', 'trainer')
admin.site.register(models.SubsToTrainer, SubsToTrainerAdmin)

class TrainersAchievementsAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(models.TrainersAchievements, TrainersAchievementsAdmin)

class TrainerSalaryAdmin(admin.ModelAdmin):
    list_display=('trainer', 'amount', 'amount_date')
admin.site.register(models.TrainerSalary, TrainerSalaryAdmin)

class TrainerNotificationAdmin(admin.ModelAdmin):
    list_display=('notif_msg',)
admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)

class NotifTrainerStatusAdmin(admin.ModelAdmin):
    list_display=('notif',)
admin.site.register(models.NotifTrainerStatus, NotifTrainerStatusAdmin)

class TrainerMsgAdmin(admin.ModelAdmin):
    list_display=('user', 'trainer', 'message')
admin.site.register(models.TrainerMsg, TrainerMsgAdmin)

class TrainerSubscriberReportAdmin(admin.ModelAdmin):
    list_display=('report_msg', 'report_a_user', 'report_a_trainer', 'reporting_trainer', 'reporting_user')
admin.site.register(models.TrainerSubscriberReport, TrainerSubscriberReportAdmin)

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)
admin.site.register(models.AppSettings, AppSettingsAdmin)