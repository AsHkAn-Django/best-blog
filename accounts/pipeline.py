

def save_user_profile(backend, user, response, *args, **kwargs):
    """Save full name from Google into the custom user model."""
    if backend.name == 'google-oauth2':
        full_name =response.get('name')
        if full_name and not user.full_name:
            user.full_name = full_name
            user.save()
