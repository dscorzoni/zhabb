from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required = True)
    password = forms.CharField(required = True)

class NewHabitForm(forms.Form):
    frequency = forms.CharField(max_length = 10, required = True)
    name = forms.CharField(max_length = 255, required = True)
    goal = forms.IntegerField()
    description = forms.CharField(max_length = 255)

class NewUserForm(forms.Form):
    username = forms.CharField(max_length = 50, required = True)
    email = forms.EmailField(required = True)
    password = forms.CharField(max_length = 50, required = True)
    confirm_password = forms.CharField(max_length = 50, required = True)