from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class ExampleTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="user_test")

    def test_create_user(self):
        test_created_user = User.objects.get(username="user_test")
        self.assertIsNotNone(test_created_user)

# Create your tests here.


