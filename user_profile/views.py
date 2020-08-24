from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, Http404, HttpResponseRedirect
from verification.models import CustomUser, ProfilePicture
from django.urls import reverse


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
    }
    try:
        context["image_url"] = profile.profilepicture.image.url
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
                    print (previous_picture.user)
            except:
                picture = ProfilePicture(user=request.user)
                picture.image = request.FILES["image"]
                picture.save()
            return HttpResponseRedirect('/user_profile/{}/'.format(_id))
    else:
        raise Http404("Page not found")
