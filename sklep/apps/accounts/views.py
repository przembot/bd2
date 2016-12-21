from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from registration.backends.simple.views import RegistrationView
from apps.accounts.forms import CustomRegistrationForm
from apps.accounts.models import Client

@sensitive_post_parameters()
@csrf_protect
@never_cache
def user_login(request):
    if request.method == 'GET':
        return auth_views.login(request, template_name="login_form.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth_views.login(request, user)
            if user.user_type == 'C':
                # TODO: change redirect
                return redirect('/')
            elif user.user_type == 'E':
                return redirect('')
            else:
                messages.error(request, "Invalid login details supplied.")
                return redirect('login')
        else:
            messages.error(request, "Invalid login details supplied.")
            return redirect('login')
    else:
        return render(request, '404.html')

class CustomRegistrationView(RegistrationView):
    template_name = 'registration_form.html'

    def get_form_class(self):
        return CustomRegistrationForm

    def register(self, form):
        new_user = super(CustomRegistrationView, self).register(form)
        Client.objects.create(user=new_user)
        return new_user

    def get_success_url(self, new_user):
        if new_user.user_type == 'C':
                # TODO: change redirect
            return '/'
        elif new_user.user_type == 'E':
            pass
