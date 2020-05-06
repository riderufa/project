"""hr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from poll.views import RegisterView, CreateUserProfile
from poll.view_poll import PollList

urlpatterns = [
    path('', PollList.as_view()),
    path('poll/', include('poll.urls', namespace='poll')),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', LoginView.as_view(template_name='poll/login.html'), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(  
        template_name='poll/register.html',  
		success_url=reverse_lazy('profile-create')  
    ), name='register'),
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)