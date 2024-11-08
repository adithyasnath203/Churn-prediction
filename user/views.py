from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login


class SignupView(TemplateView):
    template_name = "signup.html"

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get("username")
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        password1 = self.request.POST.get("password1")
        password2 = self.request.POST.get("password2")
        error = ""
        if password1 != password2:
            error = "Password not matching!"
        elif password1 is None or password2 is None:
            error = "Enter password."
        else:
            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password1,
            )
            return HttpResponseRedirect("/login")
        return render(request, self.template_name, {"error": error})


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            return render(
                request,
                self.template_name,
                {"errror": "Username of password is incorrect!"},
            )


class CustomLogoutView(LogoutView):
    next_page = "/login"
    http_method_names = ["get", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
