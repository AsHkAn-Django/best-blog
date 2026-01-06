from django.contrib.auth import get_user_model


def link_to_existing_user(strategy, details, backend, user=None, *args, **kwargs):
    """Link Google account to an existing user if the email matches."""
    if user:
        return {"is_new": False}

    email = details.get("email")
    if email:
        User = get_user_model()
        try:
            existing_user = User.objects.get(email=email)
            return {"is_new": False, "user": existing_user}
        except User.DoesNotExist:
            pass
    return {}


def save_user_profile(backend, user, response, *args, **kwargs):
    """Save full name from Google into the custom user model."""
    if backend.name == "google-oauth2":
        full_name = response.get("name")
        if full_name and not user.full_name:
            user.full_name = full_name
            user.save()
