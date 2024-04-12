from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
        
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
def send_verification_email(request,user, mail_subject,email_template ):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template ,{
        'user' : user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email,to=[to_email])
    mail.send()
    
#admin approval notification
def send_notification(mail_subject, mail_template, context):
    # Get the default sender email address from settings
    from_email = settings.DEFAULT_FROM_EMAIL
        
    # Render the email message from the template and context
    message = render_to_string(mail_template, context)
        
    # Get the recipient email address from the context
    to_email = context['user'].email
        
    # Create an EmailMessage instance
    mail = EmailMessage(mail_subject, message, from_email,to=[to_email])
    mail.send()
        
    # Set content type to HTML

        
    # Send the email
        
    
