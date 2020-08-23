from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Hello you are logged in ")
