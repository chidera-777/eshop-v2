from celery import shared_task
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, EmailMessage, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

@shared_task()
def subscriber(email):
  #news = get_object_or_404(Newsletter, id=newsletter_id)
  subject = 'Thanks for Subscribing'
  html_content = render_to_string('newsletter.html')
  text_content = strip_tags(html_content)
  msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
  msg.attach_alternative(html_content, "text/html")
  try:
      msg.send()
  except BadHeaderError:
     return HttpResponse('Invalid Header Found')