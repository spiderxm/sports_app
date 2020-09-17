from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from verification.models import Sport
import requests


# Create your views here.
def index(request):
    return render(request, "home/home.html")

def olympics(request):
    return render(request, "home/olympics.html")


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
