from django.shortcuts import redirect, render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.contrib import messages
from .models import *
from django.core.context_processors import csrf

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "sufix/registration.html"

    def form_valid(self, form):
        # проверка валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            # Создаём пользователя, если данные в форму были введены корректно.
            form.save()
            # Вызываем метод базового класса
            return super(RegisterFormView, self).form_valid(form)
        return render(self.request, 'sufix/registration.html', self.get_context_data())

class LoginFormView(FormView):
    form_class = AuthenticationForm
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "sufix/login.html"
    # В случае успеха перенаправим на главную.
    success_url = "/profile/"
    def form_valid(self, form):

        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем проверку валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            # Выполняем аутентификацию пользователя.
            auth.login(self.request, self.user)
            return super(LoginFormView, self).form_valid(form)

        return render(self.request, 'sufix/login.html', self.get_context_data())

class LogoutView(View):

    template_name = "sufix/logout.html"
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        auth.logout(request)
        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


def get_user(request):
        if request.user.is_authenticated():
            # Авторизованный пользователь.
            user = User.objects.get(pk=request.user.id)
            return render(request, 'sufix/profile.html', {'user': user})  # Пользователь авторизован.
        else:
            # Анонимный пользователь.
            raise Http404("404")