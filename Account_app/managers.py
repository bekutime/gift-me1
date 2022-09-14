from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# class UserManager(BaseUserManager):
#     """
#     Django требует, чтобы кастомные пользователи определяли свой собственный
#     класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
#     же самого кода, который Django использовал для создания User (для демонстрации).
#     """
#
#     def create_user(self, email, password=None):
#         """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
#         if email is None:
#             raise TypeError('Users must have an email address.')
#
#         user = self.model(email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#
#         return user

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    # def create_superuser(self,  email, password):
    #     """ Создает и возввращет пользователя с привилегиями суперадмина. """
    #     if password is None:
    #         raise TypeError('Superusers must have a password.')
    #
    #     user = self.create_user(email, password)
    #     user.is_superuser = True
    #     user.is_staff = True
    #     user.save()
    #
    #     return user