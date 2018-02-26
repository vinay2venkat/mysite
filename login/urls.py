from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.UserFormView.as_view(), name='register'),
    path('success/',TemplateView.as_view(template_name='login/register-success.html'), name='success'),
    #path('login/',views.UserLoginView.as_view(), name='loginpage'),
]