from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserTypeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)

            # Check if the user is an admin
            if user.is_admin and user.check_password(password):
                return user

            # If not an admin, assume the user is a regular user
            if not user.is_admin and user.check_password(password):
                return user

        except User.DoesNotExist:
            return None
