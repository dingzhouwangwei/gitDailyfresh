from  celery import Celery
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from dailyfresh2 import settings
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dailyfresh2.settings")
django.setup()


app=Celery('celery_tasks.tasks',broker='redis://192.168.178.130/9')

@app.task
def sent_register_active_mail(ss,email):
    from django.core.mail import send_mail
    subject = '天天subject'
    message = '<h1>欢迎注册，点击下面激活用户</h1><a href="http://127.0.0.1:8000/user/active/{}">http://127.0.0.1:8000/user/active/{}</a>'.format(
        ss, ss)
    sentTo = [email]
    send_mail(subject, message, settings.EMAIL_FROM,
              sentTo, html_message=message)
    return redirect(reverse('goods:index'))







