from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username, phone_number, full_name, password):
        if not phone_number:
            raise ValueError('The phone number must be set')

        if not full_name:
            raise ValueError('The full_name must be set')

        if not username:
            raise ValueError('The username must be set')

        user = self.model(phone_number=phone_number , full_name=full_name ,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, phone_number, full_name, password):
        user = self.create_user(username, phone_number, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

