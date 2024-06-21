"""
URL configuration for practicedjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import tasklist,createtask,updatetask,detailtask,deletetask

urlpatterns = [
    path('admin/', admin.site.urls),
    path('showlist/',tasklist.as_view(),name='tasklist'),
    path('Createtask/',createtask.as_view(),name='createtask'),
    path('updatetask/<int:pk>/',updatetask.as_view(),name='update'),
    path('detailview/<int:pk>',detailtask.as_view(),name='detail'),
    path('deleteview/<int:pk>',deletetask.as_view(),name='delete')

]
