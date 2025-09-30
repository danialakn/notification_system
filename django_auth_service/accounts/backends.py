# users/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User 
class PhoneOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, phone_number=None, **kwargs):

        try:
            if phone_number:
                user = User.objects.get(phone_number=phone_number)
            elif username:
                user = User.objects.get(username=username)
            else:
                return None
        except User.DoesNotExist:
            return None


        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None