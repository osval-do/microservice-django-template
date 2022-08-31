"""microservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from django.urls import include
from django.conf import settings
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    path('admin/', admin.site.urls),  
    # Add here the urls of your microservice:
      
]

# Include auth endpoints if signing key is set
if settings.JWT_SIGN_KEY:
    urlpatterns.append(path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),)
    urlpatterns.append(path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),)