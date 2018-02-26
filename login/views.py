from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from .forms import UserForm, UserLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



class UserFormView(View):
    form_class = UserForm
    template_name = 'login/register.html'

    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name,{'form':form})
    def post(self, request):
        form = self.form_class(request.POST or None )

        if form.is_valid():

            user=form.save(commit=False)
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login:success')

        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    form_class=UserLoginForm
    template_name='login/login.html'
    def get(self, request):
        form =self.form_class(None)
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form=UserLoginForm(request.POST or None)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('polls:index')

        return render(request, self.template_name, {'form':form})

def LogoutView(request):
    logout(request)
    return render(request, 'login/logout.html')



