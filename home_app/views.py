from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.urls import reverse_lazy
from .forms import AddTrial, ApplicationDetails
from verification.models import Sport, Trial, Application, DetailsOfApplication, CustomUser
import datetime
import requests
from django.contrib import messages


def home(request):
    return render(request, "home/home.html")


def olympics(request):
    return render(request, "home/olympics.html")


def trial(request):
    trials = Trial.objects.all()
    return render(request, "home/trials.html", {"trials": trials})


def sport(request):
    sports = Sport.objects.all()
    context = {
        "sports": sports
    }
    return render(request, "home/sports.html", context)


def news(request):
    url = "http://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=0c815cb62614408aaa79cdea61c866d6"
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        context = {
            "News": response["articles"],
            "No_of_articles": response["totalResults"]
        }
        return render(request, template_name="home/news.html", context=context)
    else:
        context = {
            "error": True
        }
        return render(request, template_name="home/news.html", context=context)


@login_required
def add_trial(request):
    if request.user.is_staff != True:
        raise Http404("Page not found")
    else:
        if request.method == "GET":
            form = AddTrial()
            context = {
                "form": form
            }
            return render(request, template_name="home/add_trial.html", context=context)
        else:
            form = AddTrial(request.POST)
            if form.is_valid():
                form.save()
                success_url = reverse_lazy("home:trials")
                messages.success(request, "Trial added Successfully")
                return HttpResponseRedirect(success_url)
            else:
                context = {"form": form}
                return render(request, template_name="home/add_trial.html", context=context)


@login_required
def trial_detail(request, _id):
    trial = get_object_or_404(Trial, pk=_id)
    applied = False
    try:
        application = Application.objects.get(user=request.user, trial=trial)
    except Exception as e:
        print(e)
        application = None
    if application:
        applied = True
    context = {
        "trial": trial,
        "applied": applied
    }
    return render(request, "home/trial.html", context=context)


@login_required
def apply_to_trial(request, _id):
    if request.method == "GET":
        trial = get_object_or_404(Trial, pk=_id)
        try:
            application = Application.objects.get(user=request.user, trial=trial)
        except:
            application = None
        form = ApplicationDetails()
        context = {
            "form": form,
            "trial": trial,
            "application": application
        }
        return render(request, "home/application.html", context=context)
    if request.method == "POST":
        data = request.POST
        form = ApplicationDetails(data)
        if form.is_valid():
            trial = get_object_or_404(Trial, pk=_id)
            if int(data['weight']) <= trial.max_weight and int(data['weight']) >= trial.min_weight:
                pass
            else:
                messages.error(request, "You fail the weight criteria. Better luck next time")
                success_url = reverse_lazy("home:trials")
                return HttpResponseRedirect(success_url)
            if int(data['height']) <= trial.max_height and int(data['height']) >= trial.min_height:
                pass
            else:
                messages.error(request, "You fail the height criteria. Better luck next time")
                success_url = reverse_lazy("home:trials")
                return HttpResponseRedirect(success_url)
            application = Application.objects.create(trial=trial, user=request.user, date=datetime.datetime.today())
            application.save()
            try:
                disability = data['disability']
                disability = True
            except:
                disability = False
            application_detail = DetailsOfApplication(application=application,
                                                      why_should_be_selected=data['why_should_be_selected'],
                                                      blood_group=data['blood_group'],
                                                      weight=data['weight'],
                                                      height=data['height'],
                                                      disability_details=data['disability_details'],
                                                      disability=disability
                                                      )
            application_detail.save()
            email = request.user.email
            message = f"Thanks for Applying to Trial {trial.title} \n " \
                      f"Trial Details \n Date and Time {trial.date} {trial.time} \n" \
                      f"Venue {trial.venue}\n" \
                      f"Description {trial.description}\n" \
                      f"State {trial.state} \n" \
                      f"Sport {trial.sport} \n" \
                      f"\n" \
                      f"Thanks and regards"
            send_mail(
                f"Successfully applied to {trial.title}",
                message,
                'sports.registraion@gmail.com',
                [
                    email
                ],
                fail_silently=False
            )
            messages.success(request, f"{request.user.first_name} you have successfully Applied to Trial")
            success_url = reverse_lazy("home:trials")
            return HttpResponseRedirect(success_url)
        else:
            trial = get_object_or_404(Trial, pk=_id)
            try:
                application = Application.objects.get(user=request.user, trial=trial)
            except:
                application = None
            context = {
                "form": form,
                "trial": trial,
                "application": application
            }
            return render(request, "home/application.html", context=context)


def users_list(request):
    users = CustomUser.objects.all()
    return render(request, "home/users.html", {"users": users})
