import django.test.testcases
from .models import Category, Foundation, GiveAway, Gathering, Delivery, AdditionalInfo, SiteUser
from django.contrib.auth.models import User
import tempfile


# Models Test

class ModelTest(django.test.TestCase):

    @classmethod
    def setUpTestData(cls):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        Category.objects.create(name="test_category")
        Foundation.objects.create(name="test_foundation", category_id=1)
        GiveAway.objects.create(category_id=1, foundation_id=1)
        Gathering.objects.create(count=0, place="test_place", goal="test_goal",
                                 needed_id=1, time="2010-11-20", description='test_description',
                                 photo=image)
        Delivery.objects.create(street="test_street", city='test_city', postal='test_postal012410',
                                phone='1240912400', date="2020-11-30", time="00:00", details="test_details")
        AdditionalInfo.objects.create(rules="rules_test", policy="policy_test", instruction="instructions_test")
        AdditionalInfo.objects.create(instruction="instructions_test")
        User.objects.create(username='test_user', password='test_password', email='test@mail.com')
        SiteUser.objects.create(user_id=1, gathering_id=1, donation_id=1)

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
        self.assertEqual(test_giveaway.count, 0)
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
        self.assertIsNotNone(test_gathering.photo)
        self.assertIsInstance(test_gathering, Gathering)

    def test_delivery(self):
        test_delivery = Delivery.objects.get(street='test_street')
        self.assertEqual(test_delivery.street, 'test_street')
        self.assertEqual(test_delivery.city, 'test_city')
        self.assertEqual(test_delivery.postal, 'test_postal012410')
        self.assertEqual(test_delivery.phone, 1240912400)
        self.assertEqual(test_delivery.date.year, 2020)
        self.assertEqual(test_delivery.date.day, 30)
        self.assertEqual(test_delivery.date.month, 11)
        self.assertEqual(test_delivery.time.hour, 0)
        self.assertEqual(test_delivery.time.minute, 0)
        self.assertEqual(test_delivery.details, "test_details")

    def test_additional_info(self):
        test_instructions = AdditionalInfo.objects.get(id=1)
        test_instructions2 = AdditionalInfo.objects.get(id=2)
        self.assertEqual(test_instructions.rules, "rules_test")
        self.assertEqual(test_instructions.policy, "policy_test")
        self.assertEqual(test_instructions.instruction, "instructions_test")
        self.assertEqual(test_instructions2.instruction, "instructions_test")

    def test_site_user(self):
        test_user = User.objects.get(id=1)
        self.assertIsInstance(test_user, User)
        self.assertEqual(test_user.email, 'test@mail.com')
        self.assertEqual(test_user.siteuser.gathering.place, 'test_place')
        self.assertEqual(test_user.siteuser.donation.bags, 1)
        self.assertEqual(test_user.siteuser.donation.count, 0)
