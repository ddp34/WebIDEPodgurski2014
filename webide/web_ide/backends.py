from web_ide.models import Developer
from django.contrib.auth.backends import ModelBackend

class AuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        kwargs = {'username': username}
        try:
            user = Developer.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except Developer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Developer.objects.get(pk=user_id)
        except Developer.DoesNotExist:
            return None