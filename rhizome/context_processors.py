from django.conf import settings

def custom_logo(request):
    return {'LOGO_NAME': settings.LOGO_NAME,
            'LOGO_ALT': settings.LOGO_ALT,
            'FLAG_SOP': settings.FLAG_SOP,
            'FLAG_C4D': settings.FLAG_C4D,
            'FLAG_DATA': settings.FLAG_DATA}
