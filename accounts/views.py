from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import CreateView , FormView , View
from .forms import LoginForm , RegisterForm
from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model , login , authenticate

User = get_user_model()


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = User.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.is_active:
                print("asdf ")
                user_ 					= profile
                user_.active 			= True
                user_.staff	 			= True
                user_.save()
                profile.active 			= True
                profile.activation_key  = None
                profile.save()
                return redirect("/login")
    # invalid code
    return redirect("/login")

class LoginView(FormView):
    form_class 		= LoginForm
    success_url 	= '/'
    template_name 	= 'accounts/login.html'

    def form_valid( self , form ):
        request 		= self.request
        next_ 			= request.GET.get('next')
        next_post 		= request.POST.get('next_post')
        redirect_path 	= next_ or next_post or None
        email  			= form.cleaned_data.get("email")
        password  		= form.cleaned_data.get("password")
        user 			= authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView , self).form_invalid()

class RegisterView(CreateView):
	form_class 			=  RegisterForm
	template_name		= 'accounts/register.html'
	success_url			= '/login'

