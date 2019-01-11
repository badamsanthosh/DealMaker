from django.apps import apps
from django.test import TestCase
from home_loans.apps import HomeLoansConfig


class HomeLoansConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(HomeLoansConfig.name, 'home_loans')
        self.assertEqual(apps.get_app_config('home_loans').name, 'home_loans')
