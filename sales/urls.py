from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('history',views.History,name='history'),
    path('ai_recomendation',views.AI_Recommendation,name='AI_Recommendation'),
    #path('smartshopdata',views.data_api,name='data_api'),
    
]