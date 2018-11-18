'''
Created on 11 Oct 2018

@author: Hazqeel
'''

from django.urls import path
from . import views

app_name = 'fashionClassifier'
urlpatterns = [
    path('',views.index, name = 'index'),
    path('classified/', views.classify, name = 'classify')
    ]