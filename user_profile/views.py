from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from verification.models import CustomUser


# Create your views here.
@login_required
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
    if request.method == "GET":
        return render(request, "user_profile/upload_photo.html")

    else:
        data = request.POST
        print(data)
        return redirect('user_profile/' + request.user.id + '/')
