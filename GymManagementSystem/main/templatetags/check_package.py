from django import template
from main.models import Subscription, SubPlan
from django.contrib.auth.models import User
from datetime import date, timedelta
#from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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

    try:
        user = User.objects.get(id=user_id)
        plan = SubPlan.objects.get(id=plan_id)
        check_package = Subscription.objects.filter(user=user, plan=plan).count()

        if check_package > 0:
            plan_data = Subscription.objects.filter(user=user, plan=plan).order_by('-id').first()
            today = date.today()
            sub_date = plan_data.sub_date  # Assuming sub_date is a datetime object
            plan_validity = plan_data.plan.validity_period
            expiration_date = sub_date + timedelta(days=plan_validity)
            pending_days = (expiration_date - today).days

            print(f"sub_date: {sub_date}, plan_validity: {plan_validity}, today: {today}, pending_days: {pending_days}")

            if pending_days <= 0:
                expired = True
    except (User.DoesNotExist, SubPlan.DoesNotExist) as e:
        # Handle the case where the user or plan is not found
        print(f"User or SubPlan not found: {e}")
    except Exception as e:
        # Handle other exceptions if necessary
        print(f"An error occurred: {e}")

    return expired, pending_days, plan_validity