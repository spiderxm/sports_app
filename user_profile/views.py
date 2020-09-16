from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect
from verification.models import CustomUser, ProfilePicture
from user_profile.forms import Achievement, Certificate
from django.urls import reverse_lazy
from verification.models import user_achievements, Certificates


def profile(request, _id):
    profile = get_object_or_404(CustomUser, pk=_id)
    context = {
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "age": profile.age,
        "sport": profile.sport,
        "state": profile.state,
        "email": profile.email,
        "gender": profile.gender,
        "id": profile.id,
        "achievements": None
    }
    achievements = user_achievements.objects.all().filter(user__email=context["email"])
    if len(achievements) > 0:
        context["achievements"] = achievements
    try:
        context["image_url"] = profile.profilepicture.image.url
        context["image_url"] = context["image_url"].split("?")[0]
    except:
        context["image_url"] = "https://storage.cloud.google.com/mrigankbucket/default.png"
    return render(request, "user_profile/user_profile.html", context=context)


@login_required
def upload_photo(request, _id):
    if str(request.user.id) == str(_id):
        if request.method == "GET":
            return render(request, "user_profile/upload_photo.html")

        if request.method == "POST":
            data = request.POST
            previous_picture = ProfilePicture.objects.all().filter(user=request.user)
            try:
                if previous_picture[0]:
                    previous_picture = previous_picture[0]
                    previous_picture.image = request.FILES["image"]
                    previous_picture.save()
                    print(previous_picture.user)
            except:
                picture = ProfilePicture(user=request.user)
                picture.image = request.FILES["image"]
                picture.save()
            return HttpResponseRedirect('/user_profile/{}/'.format(_id))
    else:
        raise Http404("Page not found")


@login_required
def add_achievement(request, _id):
    if str(request.user.id) == str(_id):
        if request.method == "GET":
            form = Achievement()
            return render(request, "user_profile/add_achievements.html", {"form": form})

        if request.method == "POST":
            form = Achievement(request.POST)
            if form.is_valid():
                date = form.cleaned_data["date"]
                tournament = form.cleaned_data["Name_of_Tournament"]
                venue = form.cleaned_data["Venue"]
                event = form.cleaned_data["Event"]
                Medal_won = form.cleaned_data["Medal_won"]
                achievement = user_achievements(user=request.user,
                                                date=date,
                                                Name_of_Tournament=tournament,
                                                Venue=venue,
                                                Event=event,
                                                Medal_won=Medal_won)
                achievement.save()
                print(achievement)
                return HttpResponseRedirect('/user_profile/{}/'.format(_id))
            else:

                return render(request, "user_profile/add_achievements.html", {"form": form})
    else:
        raise Http404("Page not found")


@login_required
def add_certificate(request, _id):
    if str(request.user.id) == str(_id):
        if request.method == "GET":
            form = Certificate()
            return render(request, "user_profile/add_certificates.html", {"form": form})

        if request.method == "POST":
            form = Certificate(request.POST, request.FILES)
            if form.is_valid():
                certificate = Certificates.objects.create(
                    user=request.user,
                    message=request.POST['message'],
                    certificate=request.FILES['certificate']
                )
                print(certificate)
                certificate.save()
                return HttpResponseRedirect('/user_profile/{}/'.format(_id))
            else:
                print(form.errors)
                return render(request, "user_profile/add_certificates.html", {"form": form})
    else:
        raise Http404("Page not found")
