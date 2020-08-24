from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from verification.models import Sport


# Create your views here.
@login_required
def index(request):
    return render(request, "home/home.html")


def sport(request):
    sports = Sport.objects.all()
    print (sports)
    context = {
        "sports": sports
    }
    return render(request, "home/sports.html", context)
