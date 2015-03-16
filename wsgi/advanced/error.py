import traceback
from django.conf import settings

def getTrace():
    if settings.DEBUG:
        return str(traceback.format_exc())
    else:
        return "Error Trace Not Available"