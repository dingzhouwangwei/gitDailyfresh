from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^order/',views.Order.as_view(),name='order')
]