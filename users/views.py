from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
# Create your views here.
@login_required
def profile(request):
    auth_user = request.user
    auth_userid = auth_user.id
    

    try:
        infos = Profile.objects.get(user_id=auth_userid)

    except Profile.DoesNotExist:
        user_info = Profile.objects.create(user_id=auth_user.id)
        user_info.save()
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if update_form.is_valid and profile_form.is_valid:
            update_form.save()
            profile_form.save()
    else:
        update_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm( instance=request.user.profile)
    

    
        
        
        
    context = { 'infos':infos,
                'update_form':update_form,
                'profile_form':profile_form,}
    return render(request, 'users/profile.html', context )