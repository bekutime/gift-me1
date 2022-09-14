from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from Account_app.models import MyUser, Profile


class UserCreationForm(forms.ModelForm):
    """Форма для создания новых пользователей. Включает в себя все необходимые
        полей, а также повторный пароль."""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    '''Что такое widget- Это поле будет создоваться поле'''

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        # Убедитесь, что две записи пароля совпадают
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Сохраняем предоставленный пароль в хешированном формате
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Форма для обновления пользователей. Включает в себя все поля на
      пользователя, но заменяет поле пароля на admin
      поле отображения хэша пароля.
      """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active')
#'is_staff'
    def clean_password(self):
        # Независимо от того, что предоставил пользователь, вернуть начальное значение.
        # Это делается здесь, а не на поле, т.к.
        # поле не имеет доступа к начальному значению
        return self.initial["password"]


class MyUserAdmin(BaseUserAdmin):
    # Формы для добавления и изменения пользовательских экземпляров
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, которые будут использоваться при отображении модели пользователя.
    # Они переопределяют определения в базе UserAdmin.
    # которые ссылаются на определенные поля в auth.User.
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff',)

    '''Установите fieldsets для управления макетом административных страниц «добавить» и «изменить».'''
    '''Как и в случае с fieldsопцией, чтобы отобразить несколько полей в одной строке, заключите эти поля в их собственный кортеж. 
    В этом примере поля first_nameи last_nameбудут отображаться в одной строке:
    {
    'fields': (('first_name', 'last_name'), 'address', 'city', 'state'),
    }'''
    '''     ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}), '''

    fieldsets = (
        (None, {'fields': (( 'email', 'password'))}),
        # ('Personal info', {'fields': ('email', )}),
        ('Permissions', {'fields': ('is_staff', 'groups', 'user_permissions',)}),
    )
    # add_fieldsets не является стандартным атрибутом ModelAdmin. ПользовательАдминистратор
    # переопределяет get_fieldsets для использования этого атрибута при создании пользователя.
    # Каждая секцию говорит о заголовке, в данный момент заголовок не нужен.None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'confirm_password', 'is_staff')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


#  Теперь зарегистрируйте нового UserAdmin...
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Profile)