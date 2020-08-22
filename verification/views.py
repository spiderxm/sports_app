from django.shortcuts import render, HttpResponse
from verification.forms import Register


# Create your views here.
def login(request):
    return HttpResponse("login")


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "verification/register.html", {"form": form})

        return HttpResponse("signup complete")
    else:
        form = Register
        return render(request, "verification/register.html", {"form": form})
