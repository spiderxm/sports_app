from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect
from django.template.loader import render_to_string

from verification.models import CustomUser, ProfilePicture
from user_profile.forms import Achievement, Certificate
from django.urls import reverse_lazy
from verification.models import user_achievements, Certificates, Application, DetailsOfApplication, Trial
from django.contrib import messages
import pdfcrowd
from home_app.forms import ApplicationDetails


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
        context["image_url"] = "https://storage.googleapis.com/mrigankbucket/default.png"

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
        messages.success(request, f"{request.user.first_name} you have successfully updated your image")
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
            messages.success(request, f"{request.user.first_name} you have successfully added achievement")
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
            certificate.save()
            messages.success(request, f"{request.user.first_name} you have successfully uploaded new certificate")
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
        messages.success(request, f"{request.user.first_name} you have successfully deleted certificate")
        return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
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
        messages.success(request, f"{request.user.first_name} you have successfully deleted achievement")
        return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
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
                messages.success(request,
                                 f"{request.user.first_name} {request.user.last_name} you have successfully deleted your application")
                return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
            except:
                messages.error(request, f"{request.user.first_name} you have successfully deleted your application")
                return HttpResponseRedirect(reverse_lazy("home:home"))

        except Exception as e:
            return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))
    else:
        try:
            trial = get_object_or_404(Trial, pk=_id)
            application = Application.objects.get(user=request.user, trial=trial)
            details_of_application = DetailsOfApplication.objects.get(application=application)
            return render(request, "user_profile/delete_trial_application.html")
        except:
            raise Http404("Page not found")


@login_required
def download_application(request, _id):
    if request.method == "GET":
        try:
            trial = get_object_or_404(Trial, pk=_id)
            application = Application.objects.get(user=request.user, trial=trial)
            details_of_application = DetailsOfApplication.objects.get(application=application)
            achievements = user_achievements.objects.all().filter(user_id=request.user.id)
            certificates = Certificates.objects.all().filter(user_id=request.user.id)
            client = pdfcrowd.HtmlToPdfClient('spiderxm', 'c2a76a628d51f71fb76b85b8808956c4')
            response = HttpResponse(content_type='application/pdf')
            response['Cache-Control'] = 'max-age=0'
            response['Accept-Ranges'] = 'none'
            response['Content-Disposition'] = 'attachment; filename="application.pdf"'
            html = render_to_string(template_name="user_profile/application_template.html",
                                    context={"trial": trial,
                                             "application": application,
                                             "achievements": achievements,
                                             "details_of_application": details_of_application,
                                             "certificates": certificates,
                                             "user": request.user})
            client.convertStringToStream(html, response)
            return response
        except pdfcrowd.Error:
            messages.error(request, "There is a issue with api please try again later.")
            return HttpResponseRedirect('/user_profile/{}/'.format(request.user.id))


@login_required
def update_application(request, _id):
    if request.method == "GET":
        trial = get_object_or_404(Trial, pk=_id)
        application = Application.objects.get(user=request.user, trial=trial)
        details_of_application = DetailsOfApplication.objects.get(application=application)
        form = ApplicationDetails(instance=details_of_application)
        return render(request, "user_profile/update_trial_application.html", {"form": form})
    if request.method == "POST":
        data = request.POST
        form = ApplicationDetails(data)
        if form.is_valid():
            trial = get_object_or_404(Trial, pk=_id)
            application = Application.objects.get(user=request.user, trial=trial)
            details_of_application = DetailsOfApplication.objects.get(application=application)
            success_url = '/user_profile/{}/'.format(request.user.id)
            if int(data['weight']) <= trial.max_weight and int(data['weight']) >= trial.min_weight:
                pass
            else:
                messages.error(request, "You fail the weight criteria for this Trial. Can't Update Details.")
                return HttpResponseRedirect(success_url)
            if int(data['height']) <= trial.max_height and int(data['height']) >= trial.min_height:
                pass
            else:
                messages.error(request, "You fail the height criteria for this Trial. Can't Update Details.")
                return HttpResponseRedirect(success_url)
            details_of_application.why_you_should_be_selected = data['why_you_should_be_selected']
            details_of_application.weight = data['weight']
            details_of_application.height = data['height']
            try:
                disability = data['disability']
                details_of_application.disability = True
            except:
                pass
            details_of_application.disability_details = data['disability_details']
            details_of_application.blood_group = data['blood_group']
            details_of_application.save()
            messages.success(request, "Successfully Updates Details of Application")
            return HttpResponseRedirect(success_url)
        else:
            return render(request, "user_profile/update_trial_application.html", {"form": form})
