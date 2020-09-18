from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from verification.forms import Register, Login
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
import requests


def login(request):
    if request.method == "GET":
        context = {
            "form": Login()
        }
        return render(request, "verification/login.html", context)
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                auth_login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return HttpResponseRedirect(reverse_lazy('home:home'))
            else:
                context = {
                    "form": Login(request.POST),
                    "message": "Invalid Credetials Provided"
                }
                return render(request, "verification/login.html", context)

        else:
            context = {
                "form": form
            }
            return render(request, "verification/login.html", context)


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            response = requests.post(url, data=values)
            result = response.json()
            if result['success']:
                form.save()
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                age = form.cleaned_data['age']
                sport = form.cleaned_data['sport']
                state = form.cleaned_data['state']
                message = '''Thanks for registering with us. \n Details you provided are as follows: \n first-name {} \n last-name {} \n email {} \n age {}  \n sport {} \n state {} \n\n\n Thanks and Regards'''.format(
                    first_name,
                    last_name,
                    email,
                    age,
                    sport,
                    state)
                try:
                    send_mail(
                        'Account Signup on Sports Registration Application',
                        message,
                        'sports.registraion@gmail.com',  # Admin
                        [
                            email
                        ],
                        fail_silently=False
                    )
                except Exception as e:
                    print(e)
            else:
                return render(request, "verification/register.html",
                              {"form": form, "message": "Invalid reCAPTCHA. Please try again."})

        else:
            return render(request, "verification/register.html", {"form": form})

        return HttpResponseRedirect(reverse_lazy("login"))
    else:
        form = Register
        return render(request, "verification/register.html", {"form": form})


@login_required
def Logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home:home'))
    else:
        return render(request, 'verification/logout.html', context={})
