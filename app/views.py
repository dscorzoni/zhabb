from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import hashers
from django.db.models import Count

from .models import (
    Habit,
    HabitLog
)
from .forms import (
    LoginForm,
    NewHabitForm,
    NewUserForm
)



class IndexView(View):
    '''
    Render the login page if user is not logged-in.
    Otherwise, redirect user to the HabitsMain view.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('habits')
        else:
            return render(request, 'index.html', {})





class AuthView(View):
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

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('index')





class HabitsMainView(View):
    def get(self, request):
        '''
        Each day the user access the HabitsMainView, a list of habits will be added to the HabitLog table.
        If the user has accessed this view before, just show the list of habits for that day.
        '''
        if request.user.is_authenticated:
            habits = Habit.objects.filter(user = request.user)
            habit_ids = [habit.id for habit in habits]
            habits_log = HabitLog.objects.filter(habit__in = habit_ids, date_event = datetime.now().date())
            if not habits_log:
                for habit in habits:
                    new_habit_log = HabitLog(habit = habit, status = False, date_event = datetime.now().date())
                    new_habit_log.save()
            habits_out = HabitLog.objects.filter(habit__in = habit_ids, date_event = datetime.now().date())
            return render(request, 'habits.html', {"habits": habits_out})
        else:
            return redirect('index')




class HabitLogView(View):
    '''
    Toggle the status of a habit and redirect to habits page.
    '''
    def get(self, request, pk):
        habit_log = HabitLog.objects.get(id = pk)
        habit_log.status = not habit_log.status
        habit_log.save()
        return redirect('habits')




class NewHabit(View):
    '''
    The NewHabit view has get and post methods to display or add new habits through a form submitted by the user.
    GET: renders the new habit page if user is authenticated. Otherwise redirects to index for log-in.
    POST: add a new habit to database.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'new_habit.html', {})
        else:
            return redirect('index')

    def post(self, request):
        form = NewHabitForm(request.POST)
        if form.is_valid():
            new_habit = Habit(
                user = request.user,
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                goal = form.cleaned_data['goal'],
                frequency = form.cleaned_data['frequency'],
                date_start = datetime.now().date()
            )
            new_habit.save()
            new_habit_log = HabitLog(
                habit = new_habit,
                status = False,
                date_event = datetime.now().date()
            )
            new_habit_log.save()
            return redirect('habits')
        else:
            return render(request, 'new_habit.html', {'message':'All fields are required.'})





class NewUser(View):
    '''
    NewUser view has get and post methods to handle new users.
    GET: If the user is authenticated, they are redirected to the habits URL. Otherwise they are rendered the new user page.
    POST: Handle user registration with checks on existing username and password matching.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('habits')
        else:
            return render(request, 'new_user.html', {})

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            # Check if username exists:
            try:
                new_user = User.objects.get(username = form.cleaned_data['username'])
                if new_user:
                    return render(request, 'new_user.html', {'message': 'This username already exist, choose a new one.'})
            except ObjectDoesNotExist:
                if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                    new_user = User(
                        username = form.cleaned_data['username'],
                        email = form.cleaned_data['email'],
                        password = hashers.make_password(form.cleaned_data['password'])
                        )
                    new_user.save()
                    return render(request, 'index.html', {'message': 'User is created, you can log-in now.'})
                else:
                    return render(request, 'new_user.html', {'message': 'Passwords are not matching.'})
        else:
            return render(request, 'new_user.html', {'message': 'Form is invalid.'})




class ProgressCheck(View):
    '''
    ProgressCheck view only has a GET method, to display the summary stats of habits logged in the system.
    User needs to be authenticated, if not they will be redirected to index page for log-in.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            user_habits = Habit.objects.filter(user = request.user)
            habits_logs = HabitLog.objects.filter(habit__in = user_habits).values('habit__name', 'status').annotate(count = Count('id')).order_by()

            # Parsing results to return one object per habit
            habits_output = []
            for habit in user_habits:
                habit_output = {}
                single_habit = habits_logs.filter(habit__name = habit.name)
                for row in single_habit:
                    if row['status'] == False:
                        habit_output['name'] = row['habit__name']
                        habit_output['status_false'] = row['count']
                    else:
                        habit_output['name'] = row['habit__name']
                        habit_output['status_true'] = row['count']
                if 'status_false' not in habit_output:
                    habit_output['total_days'] = habit_output['status_true']
                    habit_output['complete_rate'] = 100
                elif 'status_true' not in habit_output:
                    habit_output['total_days'] = habit_output['status_false']
                    habit_output['complete_rate'] = 0
                else:
                    habit_output['total_days'] = habit_output['status_false'] + habit_output['status_true']
                    habit_output['complete_rate'] = round(float(habit_output['status_true'] / habit_output['total_days'])*100,1)
                habits_output.append(habit_output)

            return render(request, 'progress_check.html', {'habits': habits_output})
        else:
            return redirect('index')
