from django.core.exceptions import ValidationError
import os

def allow_image_only(value):
    ext = os.path.splitext(value.name)[1]   #cover.jpg '[1]' that is index number for cover.jpg.so index one is jpg. 
    print(ext)
    valid_extension = ['.jpg','.png','.jpeg']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension. Allow extension : ' +str(valid_extension))