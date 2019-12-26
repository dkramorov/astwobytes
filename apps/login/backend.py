from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class MyBackend(ModelBackend):
    """Авторизация с select_related('customuser')"""
    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.select_related('customuser').get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

