from django.contrib import admin
from django.urls import path
from visualization import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    
   
    path('', views.idp_visualization, name='idp_visualization'),
]
