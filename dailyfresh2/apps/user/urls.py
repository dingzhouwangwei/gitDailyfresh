from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    # url(r'^register/',views.Register.as_view(),name='register'),
    # url(r'^active/(?P<str>.*)/',views.active,name='active')
    url(r'^active/(?P<str>.*)', views.Active.as_view(), name='active'),
    url(r'^login', views.Login.as_view(), name='login'),
    url(r'^logout', views.Logout.as_view(), name='logout'),
    url(r'^info', views.Info.as_view(), name='info'),
    url(r'^order', views.Order.as_view(), name='order'),
    url(r'^address', views.Addresss.as_view(), name='address'),

]