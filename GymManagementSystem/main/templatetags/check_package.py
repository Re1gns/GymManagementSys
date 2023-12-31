from django import template
from main.models import Subscription, SubPlan
from django.contrib.auth.models import User
from datetime import date
register = template.Library()

@register.simple_tag
def check_purchased_package(user_id, plan_id):
    user = User.objects.get(id=user_id)
    plan = SubPlan.objects.get(id=plan_id)
    check_package = Subscription.objects.filter(user=user, plan=plan).count()
    if check_package > 0:
        return True
    else:
        return False
    
@register.simple_tag
def check_plan_validity(user_id, plan_id):
    expired = False
    pending_days = None
    plan_validity = None
    user = User.objects.get(id=user_id)
    plan = SubPlan.objects.get(id=plan_id)
    check_package = Subscription.objects.filter(user=user, plan=plan).count()
    if check_package > 0:
        plan_data = Subscription.objects.filter(user=user, plan=plan).order_by('-id').first()
        today = date.today()
        pdate = plan_data.sub_date
        pending_days = (today - pdate).days
        plan_validity = plan_data.plan.validity_period
        if plan_validity < pending_days:
            expired = True
    else:
        False
    return pending_days