from django.urls import path

from . import api

urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:pk>/', api.read_notifications, name='read_notifications'),
]
