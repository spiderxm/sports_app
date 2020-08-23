from django.shortcuts import render, HttpResponse
from verification.forms import Register, Login
from django.core.mail import send_mail


# Create your views here.
def login(request):
    form = Login()
    
    return HttpResponse("login")


def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            sport = form.cleaned_data['sport']
            state = form.cleaned_data['state']
            message = '''Thanks for registering with us. \n Details you provided are as follows: \n first-name {} \n last-name {} \n email {} \n age {}  \n sport {} \n state {}'''.format(
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
                print (e)
        else:
            return render(request, "verification/register.html", {"form": form})

        return HttpResponse("signup complete")
    else:
        form = Register
        return render(request, "verification/register.html", {"form": form})
