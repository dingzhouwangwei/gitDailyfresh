from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^active/(?P<str>.*)/',views.active,name='active'),
]