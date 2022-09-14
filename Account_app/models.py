from django.utils.translation import gettext as _
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from Account_app.managers import UserManager

''' Профиль пользователя'''
class Profile(models.Model):

    user = models.OneToOneField('MyUser', on_delete=models.CASCADE)
    name = models.CharField(_('nickname'), max_length=150, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    # email = models.OneToOneField('MyUser', on_delete=models.CASCADE,)
    # email = models.EmailField(_("Email address"), )
    bio = models.TextField(_('bio'), max_length=140, blank=True)
    avatarka = models.ImageField(_('Avatarka'), upload_to='Avatarka', null=True, blank= True)
    phone_number = models.CharField(_("phone number"), max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    instagram = models.URLField('Ссылка на Instagram', max_length=300)
    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        unique_together = ('name', 'phone_number')


    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, будем возвращать username.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


'''Тут создаем Пользователя'''
class MyUser(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    # username = models.CharField(_("username"), db_index=True, max_length=255, unique=True)

    # Так же мы нуждаемся в поле, с помощью которого будем иметь возможность
    # связаться авторизовать его при входе в систему.
    # Поскольку адрес почты нам нужен в любом случае, мы также будем
    # использовать его для входы в систему, так как это наиболее
    # распространенная форма учетных данных на данный момент (ну еще телефон).
    email = models.EmailField(_("email address"), unique=True)



    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False)

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)



    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    # @property
    # def token(self):
    #     """
    #     Позволяет получить токен пользователя путем вызова user.token, вместо
    #     user._generate_jwt_token(). Декоратор @property выше делает это
    #     возможным. token называется "динамическим свойством".
    #     """
    #     return self._generate_jwt_token()



    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + timedelta(days=1)
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token.decode('utf-8')



