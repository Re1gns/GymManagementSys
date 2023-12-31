from . import models

def get_logo(request):
    logo = models.AppSettings.objects.first()
    data = {
        'logo':logo.image_tag
    }
    return data