import unittest
import django.test.testcases
from .models import Category, Foundation, GiveAway, Gathering, AdditionalInfo, SiteUser
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .forms import CustomUserCreationForm


# Connection Tests


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_landing_page(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 302)


# Form Tests

class FormTest(unittest.TestCase):

    def test_form_valid(self):
        form = CustomUserCreationForm(data={'password1': 'Mkonjibhu7!',
                                            'password2': 'Mkonjibhu7!', 'email': 'tester@mail.com'})
        self.assertTrue(form.is_valid())

    def test_form_password_length(self):
        form = CustomUserCreationForm(data={'password1': '1234567',
                                            'password2': '1234567', 'email': 'tester@mail.com'})
        self.assertFalse(form.is_valid())

    def test_form_password_without_special_sign(self):
        form = CustomUserCreationForm(data={'password1': 'Mkonjibhu7',
                                            'password2': 'Mkonjibhu7', 'email': 'tester@mail.com'})
        self.assertFalse(form.is_valid())

    def test_form_mail_invalid(self):
        form = CustomUserCreationForm(data={'password1': 'Mkonjibhu7!',
                                            'password2': 'Mkonjibhu7!', 'email': 'testermailwithoutat.com'})
        self.assertFalse(form.is_valid())


# Models Test

class ModelTest(django.test.TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="test_category")
        Foundation.objects.create(name="test_foundation", category_id=1)
        GiveAway.objects.create(category_id=1, foundation_id=1)

        AdditionalInfo.objects.create(rules="rules_test", policy="policy_test", instruction="instructions_test")
        AdditionalInfo.objects.create(instruction="instructions_test")
        SiteUser.objects.create(user_id=1, donation_id=1, phone=1241231, date='2019-03-30')
        Gathering.objects.create(place="test_place", goal="test_goal",
                                 needed_id=1, time="2010-11-20", description='test_description', person_id=1)
        User.objects.create(username='test_user', password='test_password', email='test@mail.com')

    def test_category(self):
        test_category = Category.objects.get(name='test_category')
        self.assertEqual(test_category.name, "test_category")
        self.assertIsInstance(test_category, Category)

    def test_foundation(self):
        test_foundation = Foundation.objects.get(name="test_foundation")
        self.assertEqual(test_foundation.name, 'test_foundation')
        self.assertEqual(test_foundation.category.name, 'test_category')
        self.assertIsInstance(test_foundation, Foundation)

    def test_giveaway(self):
        test_giveaway = GiveAway.objects.get(category_id=1)
        self.assertEqual(test_giveaway.category.id, 1)
        self.assertEqual(test_giveaway.bags, 1)
        self.assertEqual(test_giveaway.foundation.name, "test_foundation")
        self.assertIsInstance(test_giveaway, GiveAway)

    def test_gathering(self):
        test_gathering = Gathering.objects.get(place="test_place")
        self.assertEqual(test_gathering.place, "test_place")
        self.assertEqual(test_gathering.goal, "test_goal")
        self.assertEqual(test_gathering.needed_id, 1)
        self.assertEqual(test_gathering.time.year, 2010)
        self.assertEqual(test_gathering.time.day, 20)
        self.assertEqual(test_gathering.time.month, 11)
        self.assertEqual(test_gathering.description, "test_description")
        self.assertIsInstance(test_gathering, Gathering)

    def test_additional_info(self):
        test_instructions = AdditionalInfo.objects.get(id=1)
        test_instructions2 = AdditionalInfo.objects.get(id=2)
        self.assertEqual(test_instructions.rules, "rules_test")
        self.assertEqual(test_instructions.policy, "policy_test")
        self.assertEqual(test_instructions.instruction, "instructions_test")
        self.assertEqual(test_instructions2.instruction, "instructions_test")

    def test_site_user(self):
        test_user = SiteUser.objects.get(id=1)
        self.assertIsInstance(test_user, SiteUser)
        self.assertEqual(test_user.user.email, 'test@mail.com')
        self.assertEqual(test_user.donation.bags, 1)


class RegistrationViewTestCase(django.test.TestCase):

    def test_registration_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'register.html')
        self.failUnless(isinstance(response.context['form'],
                                   CustomUserCreationForm))

    def test_registration_view_post_success(self):
        response = self.client.post(reverse('register'),
                                    data={'email': 'test@test.com',
                                          'password1': 'Mkonjibhu7!', 'password2': 'Mkonjibhu7!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_registration_view_post_failure(self):
        response = self.client.post(reverse('register'),
                                    data={'email': 'test@test.com',
                                          'password1': 'pass_to_fail', 'password2': 'mkonjibhu'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
