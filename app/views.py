from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout

from .forms import (
    LoginForm
)



class Index(View):
    '''
    Render the login page if user is not logged-in.
    Otherwise, redirect user to the HabitsMain view.
    --- To be implemented
    '''
    def get(self, request):
        return render(request, 'index.html', {})





class Auth(View):
    '''
    Implements authentication logic.
    POST:
        If successful, redirect users to Habits page.
        If fail, render to index.html with error message.
    GET:
        Redirects to index page.
    '''
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('habits')

        return render(request, 'index.html', {'message':'User or password invalid.'})

    def get(self, request):
        return redirect('index')

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')





class HabitsMain(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'habits.html', {})
        else:
            return redirect('index')