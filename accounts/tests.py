from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Address, UserProfile


class UserProfileTest(TestCase):
    def test_profile_auto_created_on_user_create(self):
        user = User.objects.create_user(username="newuser", password="password")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_profile_str(self):
        user = User.objects.create_user(username="struser", password="password")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), "struser")


class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="addruser", password="password")

    def test_create_shipping_address(self):
        address = Address.objects.create(
            user=self.user,
            street_address="123 Main St",
            apartment_address="Apt 4",
            country="US",
            zip="10001",
            address_type="S",
        )
        self.assertEqual(str(address), "123 Main St, US")
        self.assertEqual(address.address_type, "S")

    def test_user_can_have_multiple_addresses(self):
        Address.objects.create(
            user=self.user, street_address="1 St", apartment_address="",
            country="US", zip="10001", address_type="S",
        )
        Address.objects.create(
            user=self.user, street_address="2 Ave", apartment_address="",
            country="US", zip="10002", address_type="B",
        )
        self.assertEqual(Address.objects.filter(user=self.user).count(), 2)
