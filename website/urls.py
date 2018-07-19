from django.conf.urls import url
from rest_framework import views

urlpatterns = [

    url(r'^rest_example$', views.APIView.as_view()),
    url(r'^rest_example/(?P<pk>[0-9]+)/$', views.APIView.as_view()),

    ]
