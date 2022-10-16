from io import BytesIO
from celery import shared_task
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from .models import Customer

@shared_task()
def payment_completed(customer_id):
    '''
    Task to send Emails to user when an order is completed
    '''
    order = get_object_or_404(Customer, id=customer_id)
    subject = f"Eshop - Invoice no. {order.id}"
    message = "Here are the details of your recent purchase"
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user, 'ferdinandchidera49@gmail.com'])
    
    # generate PDF
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    HTML(string=html).write_pdf(out, stylesheets=[CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')])
    
    # attach PDF
    email.attach('order.pdf', out.getvalue(), 'application/pdf')
    try:
        email.send()
    except BadHeaderError:
      return HttpResponse('Invalid header found')