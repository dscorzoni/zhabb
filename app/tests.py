from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from .models import (
    Habit
)

#########################
# URL status code tests #
#########################

class UrlTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='pass1',
            email='user@user.com'
        )

    def test_url_get_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_url_get_newuser(self):
        response = self.client.get(reverse('newuser'))
        self.assertEqual(response.status_code, 200)

    def test_url_get_auth(self):
        # Test if it returns status 302 (redirect to index)
        response = self.client.get(reverse('auth'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_logout(self):
        # Test if it returns status 302 (redirect to index)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_habits(self):
        # Test if it returns status 302 (if not logged, redirect to index)
        response = self.client.get(reverse('habits'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_new_habit(self):
        # Test if it returns status 302 (if not logged, redirect to index)
        response = self.client.get(reverse('new-habit'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_habits_check(self):
        # Test if it returns status 302 (if not logged, redirect to index)
        response = self.client.get(reverse('habits-check', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_url_get_progress(self):
        # Test if it returns status 302 (if not logged, redirect to index)
        response = self.client.get(reverse('progress'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_logged_index(self):
        # Test if a logged user access index page, it should return 302 redirect to habits.
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_logged_newuser(self):
        # Test if a logged user access newuser page, it should return 302 redirect to habits.
        self.client.force_login(self.user)
        response = self.client.get(reverse('newuser'))
        self.assertEqual(response.status_code, 302)

    def test_url_get_logged_habits(self):
        # If logged, should return status 200
        self.client.force_login(self.user)
        response = self.client.get(reverse('habits'))
        self.assertEqual(response.status_code, 200)

    def test_url_get_logged_new_habit(self):
        # If logged, should return status 200
        self.client.force_login(self.user)
        response = self.client.get(reverse('new-habit'))
        self.assertEqual(response.status_code, 200)

    def test_url_get_logged_progress(self):
        # If logged, should return status 200
        self.client.force_login(self.user)
        response = self.client.get(reverse('progress'))
        self.assertEqual(response.status_code, 200)

    def test_url_post_auth_success(self):
        # If login successfully, it should redirect to habits (302)
        response = self.client.post(reverse('auth'), {'username':'user1', 'password':'pass1'})
        self.assertEqual(response.status_code, 302)

    def test_url_post_auth_fail(self):
        # If wrong username/password, it should return status 200 and render index
        response = self.client.post(reverse('auth'), {'username':'user', 'password':'pass'})
        self.assertEqual(response.status_code, 200)

    def test_url_post_new_habit_success(self):
        # Redirects to habits if successful (302)
        self.client.force_login(self.user)
        response = self.client.post(reverse('new-habit'), {
            'user': self.user,
            'name': 'Habit',
            'description': 'Habit description.',
            'goal': 1,
            'frequency': 'weekly',
            'date_start': datetime.now().date()
        })
        self.assertEqual(response.status_code, 302)

    def test_url_post_new_habit_incomplete(self):
        # Render page with error message if missing info (200)
        self.client.force_login(self.user)
        response = self.client.post(reverse('new-habit'), {})
        self.assertEqual(response.status_code, 200)





#########################
# View Tests            #
#########################

class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='pass1',
            email='user@user.com'
        )

    def test_url_post_auth_wrong_user(self):
        response = self.client.post(reverse('auth'), {'username':'user', 'password':'pass'})
        self.assertContains(response, 'User or password invalid.')

    def test_url_post_newuser_success(self):
        # If new user created succesfully
        response = self.client.post(reverse('newuser'), {'username':'user2', 'password':'pass2', 'email':'email@email.com', 'confirm_password':'pass2'})
        self.assertContains(response, 'User is created, you can log-in now.')

    def test_url_post_newuser_empty_form(self):
        # Trying to submit empty form
        response = self.client.post(reverse('newuser'), {})
        self.assertContains(response, 'Form is invalid.')

    def test_url_post_newuser_user_exists(self):
        # Trying to submit empty form
        response = self.client.post(reverse('newuser'), {'username':'user1', 'password':'pass1', 'email':'email@email.com', 'confirm_password':'pass1'})
        self.assertContains(response, 'This username already exists, choose a new one.')

    def test_url_post_newuser_password_mismatch(self):
        # Password mismatch
        response = self.client.post(reverse('newuser'), {'username':'user2', 'password':'pass2', 'email':'email@email.com', 'confirm_password':'pass3'})
        self.assertContains(response, 'Passwords are not matching.')

    def test_url_post_new_habit_incomplete(self):
        # Render page with error message if missing info (200)
        self.client.force_login(self.user)
        response = self.client.post(reverse('new-habit'), {})
        self.assertContains(response, 'All fields are required.')

    def test_url_get_habits_list_empty(self):
        # Render the habits list page (empty list)
        self.client.force_login(self.user)
        response = self.client.get(reverse('habits'))
        self.assertContains(response, 'add habits using the button below:')

    def test_url_get_habits_list_filled(self):
        # Render the habits list page (filled list)
        self.client.force_login(self.user)
        create_habit = self.client.post(reverse('new-habit'), {
            'user': self.user,
            'name': 'Habit',
            'description': 'Habit description.',
            'goal': 1,
            'frequency': 'weekly',
            'date_start': datetime.now().date()
        })
        response = self.client.get(reverse('habits'))
        self.assertContains(response, 'here are your habits:')

    def test_url_get_progress_non_empty(self):
        # Progress page with non empty list of habits.
        self.client.force_login(self.user)
        create_habit = self.client.post(reverse('new-habit'), {
            'user': self.user,
            'name': 'Habit',
            'description': 'Habit description.',
            'goal': 1,
            'frequency': 'weekly',
            'date_start': datetime.now().date()
        })
        response = self.client.get(reverse('progress'))
        self.assertContains(response, 'Each habit has a complete rate, which means how many days you completed the habit divided by the total days logged in the app.')

    def test_url_get_progress_empty(self):
        # Progress page with empty list of habits.
        self.client.force_login(self.user)
        response = self.client.get(reverse('progress'))
        self.assertContains(response, 'You need to add habits to check progress in this page.')