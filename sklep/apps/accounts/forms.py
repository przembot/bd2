from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationForm
import django.forms as forms


class CustomRegistrationForm(RegistrationForm):
    first_name  = forms.CharField(required=True)
    last_name   = forms.CharField(required=True)
    address     = forms.CharField(required=True)
    birth_date  = forms.DateField(required=True,
                                  input_formats=['%d/%m/%Y'],
                                  help_text='Date format: day/month/year')

    field_order = ['username', 'first_name', 'last_name','password1',
                   'password2', 'email', 'birth_date', 'address']

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.user_type = 'C'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birthdate = self.cleaned_data['birth_date']
        user.adress = self.cleaned_data['address']
        if commit:
            user.save()
        return user
