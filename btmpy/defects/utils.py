from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_view(email):
    subject = 'You have assigned a defect complete ASAP'
    message = 'The given High Priority Defect Need to complete'
    from_email = 'sworajtadudemo@gmail.com'  #host email
    recipient_list = [email] #email address of recipientt

    #render html page for template
    html_message = render_to_string('defects/task_email_template.html')
    #create plaintext version by striping html tag
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return HttpResponse('Email sent Successfully! ')
    except Exception as e:
        return HttpResponse(f"Error sending email : {str(e)}")