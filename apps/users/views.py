from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import UserLoginForm

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email = email , password=password)
        auth_login(request, user)
        if next:
            return redirect(next)
    context = {
        'form': form
    }
    return render(request,'login.html', context=context)