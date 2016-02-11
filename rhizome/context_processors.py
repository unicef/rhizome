from django.conf import settings

def custom_logo(request):
    return {'LOGO_NAME': settings.LOGO_NAME, 'LOGO_ALT': settings.LOGO_ALT}
