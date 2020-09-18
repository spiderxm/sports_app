from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect
from verification.models import CustomUser, ProfilePicture
from user_profile.forms import Achievement, Certificate
from django.urls import reverse_lazy
from verification.models import user_achievements, Certificates, Application, DetailsOfApplication, Trial


def profile(request, _id):
    profile = get_object_or_404(CustomUser, pk=_id)
    context = {
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "age": profile.age,
        "date_joined": profile.date_joined,
        "sport": profile.sport,
        "state": profile.state,
        "email": profile.email,
        "gender": profile.gender,
        "id": profile.id,
        "achievements": None
    }
    if str(request.user.id) == str(_id):
        trials_applied_to = Application.objects.all().filter(user=request.user)
        if len(trials_applied_to) == 0:
            context['trials_applied_to'] = None
            context['noshow'] = True
        context['trials_applied_to'] = trials_applied_to
    else:
        context['noshow'] = True
    achievements = user_achievements.objects.all().filter(user__email=context["email"])
    if len(achievements) > 0:
        context["achievements"] = achievements
        context["no_achievements"] = len(achievements)
    else:
        context["no_achievements"] = 0
    certificates = Certificates.objects.all().filter(user__email=context["email"])
    if len(certificates) > 0:
        context["certificates"] = certificates
        context["no_certificates"] = len(certificates)
    else:
        context["no_certificates"] = 0
    try:
        context["image_url"] = profile.profilepicture.image.url
        context["image_url"] = context["image_url"].split("?")[0]
    except:
        context["image_url"] = "https://storage.cloud.google.com/mrigankbucket/default.png"

    Applications = Application.objects.all().filter(user_id=profile.id)
    if str(request.user.id) == str(_id):
        context["applications"] = Applications
    else:
        context["applications"] = None
    context["no_applications"] = len(Applications)
    return render(request, "user_profile/user_profile.html", context=context)


@login_required
def upload_photo(request):
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
        return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))


@login_required
def add_achievement(request):
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
            return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
        else:
            return render(request, "user_profile/add_achievements.html", {"form": form})


@login_required
def add_certificate(request):
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
            return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
        else:
            print(form.errors)
            return render(request, "user_profile/add_certificates.html", {"form": form})


@login_required
def view_trial_application_details(request, _id):
    try:
        trial = get_object_or_404(Trial, pk=_id)
        application = Application.objects.get(user=request.user, trial=trial)
        details_of_application = DetailsOfApplication.objects.get(application=application)
        context = {
            "trial": trial,
            "application": application,
            "details": details_of_application
        }
        return render(request, template_name="user_profile/trial_info.html", context=context)
    except Exception as e:
        print(e)
        raise Http404("Page not found")


@login_required
def delete_certificate(request, _id):
    if request.method == "POST":
        certificate = get_object_or_404(Certificates, pk=_id)
        if certificate.user == request.user:
            certificate.delete()
        return HttpResponseRedirect(reverse_lazy("home:home"))
    if request.method == "GET":
        certificate = get_object_or_404(Certificates, pk=_id)
        if certificate.user != request.user:
            return Http404("Page not found")
        return render(request, "user_profile/delete_certificate.html")


@login_required
def delete_achievement(request, _id):
    if request.method == "POST":
        achievement = get_object_or_404(user_achievements, pk=_id)
        if achievement.user == request.user:
            achievement.delete()
        return HttpResponseRedirect(reverse_lazy("home:home"))
    if request.method == "GET":
        achievement = get_object_or_404(user_achievements, pk=_id)
        if achievement.user != request.user:
            return Http404("Page not found")
        return render(request, "user_profile/delete_achievement.html")


@login_required
def delete_trial_application(request, _id):
    if request.method == "POST":
        try:
            trial = get_object_or_404(Trial, pk=_id)
            application = Application.objects.get(user=request.user, trial=trial)
            details_of_application = DetailsOfApplication.objects.get(application=application)
            try:
                details_of_application.delete()
                application.delete()
                return HttpResponseRedirect(reverse_lazy("home:home"))
            except:
                return HttpResponseRedirect(reverse_lazy("home:home"))

        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse_lazy("home:home"))
    else:
        try:
            trial = get_object_or_404(Trial, pk=_id)
            application = Application.objects.get(user=request.user, trial=trial)
            details_of_application = DetailsOfApplication.objects.get(application=application)
            return render(request, "user_profile/delete_trial_application.html")
        except:
            raise Http404("Page not found")
