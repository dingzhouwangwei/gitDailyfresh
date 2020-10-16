from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^cart', views.cart.as_view(), name='cart'),
]