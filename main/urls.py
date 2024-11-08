from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path

from user.views import SignupView, LoginView, CustomLogoutView
from functions.views import Home, ChurnFinderView, SendEmailView, BulkChurnFinder, BulkEmailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name ="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("home/", Home.as_view(), name="home"),
    path("churn-finder/", ChurnFinderView.as_view(), name="churn-finder"),
    path("send-email/", SendEmailView.as_view(), name='send_email'),
    path("bulk-check/", BulkChurnFinder.as_view(), name="bulk_check"),
    path("bulk-send/", BulkEmailView.as_view(), name="bulk_send"),
]
