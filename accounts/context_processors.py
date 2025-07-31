from .models import profile

def profile_context(request):
    # Only try to get a profile if the user is logged in
    if request.user.is_authenticated:
        try:
            # Get the profile linked to the current user
            prof = request.user.profile
            # Return it in a dictionary
            return {'prof': prof}
        except profile.DoesNotExist:
            # If a user has no profile for some reason, return an empty dict
            return {}
    # If the user is not logged in, return an empty dict
    return {}