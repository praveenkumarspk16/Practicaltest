from django.conf.urls import url

from crud import views

urlpatterns = [
    url(r'^create$',views.create,name='create'),
    url(r'^index$',views.index,name='index'),
    url(r'^update/(?P<id>[0-9]+)$',views.update,name='update'),
    url(r'^delete/(?P<id>[0-9]+)$',views.delete,name='delete'),
    url(r'^view/(?P<id>[0-9]+)$',views.views,name='view'),

]