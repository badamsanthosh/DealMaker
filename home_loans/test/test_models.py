from django.test import TestCase
from home_loans.models import Loan, AmountRange
from test import get_database_name
import sys
import pdb


class LoanTest(TestCase):
    """
    Test Module for Loan Test
    """

    product_name = "Standard Fixed (P & I) - Owner Occupied"
    brand_name = "Bank of Queensland"
    channel_path = "personal"
    owner_id = 10
    brand_path = "boq"
    display_name = "Standard Fixed 1 Year"
    description = "Standard Fixed (P & I) - Owner Occupied"
    rate_type = "fixed"
    fixed_term = 1
    min_amount = 100000
    max_amount = 9999999
    max_lvr = 80
    rate = 5.61
    frequencies = ['weekly', 'fortnightly', 'monthly']

    def setUp(self):
        Loan.objects.all().delete()
        self.db_name = get_database_name()
        if not self.db_name.startswith('test'):
            sys.exit(1)
        Loan.objects.create(product_name=LoanTest.product_name, brand_name=LoanTest.brand_name,
                            channel_path=LoanTest.channel_path, owner_id=LoanTest.owner_id,
                            brand_path=LoanTest.brand_path, display_name=LoanTest.display_name,
                            description=LoanTest.description, rate_type=LoanTest.rate_type,
                            fixed_term=LoanTest.fixed_term, min_amount=LoanTest.min_amount,
                            max_amount=LoanTest.max_amount, max_lvr=LoanTest.max_lvr, rate=LoanTest.rate,
                            frequencies=LoanTest.frequencies)

    def test_loan_str(self):
        loan_obj = Loan.objects.get(product_name=LoanTest.product_name)
        self.assertEqual(
            loan_obj.__str__(), LoanTest.product_name
        )

    def tearDown(self):
        """
        Truncate the Loan Table
        :return:
        """
        if self.db_name.startswith('test'):
            Loan.objects.all().delete()


class AmountRangeTest(TestCase):
    """
    Test Module for Amount Range
    """

    loan_id = Loan.objects.create(product_name=LoanTest.product_name, brand_name=LoanTest.brand_name,
                                  channel_path=LoanTest.channel_path, owner_id=LoanTest.owner_id,
                                  brand_path=LoanTest.brand_path, display_name=LoanTest.display_name,
                                  description=LoanTest.description, rate_type=LoanTest.rate_type,
                                  fixed_term=LoanTest.fixed_term, min_amount=LoanTest.min_amount,
                                  max_amount=LoanTest.max_amount, max_lvr=LoanTest.max_lvr, rate=LoanTest.rate,
                                  frequencies=LoanTest.frequencies).loan_id
    loan_obj = Loan.objects.get(loan_id=loan_id)
    min_amount = 20000
    max_amount = 50000

    def setUp(self):
        self.db_name = get_database_name()
        if not self.db_name.startswith('test'):
            sys.exit(1)

        self.ar_id = AmountRange.objects.create(
            loan_id=AmountRangeTest.loan_obj,
            min_amount=AmountRangeTest.min_amount,
            max_amount=AmountRangeTest.max_amount).amount_range_id

    def test_amount_range_str(self):
        ar_obj = AmountRange.objects.get(loan_id=AmountRangeTest.loan_obj,
                                         min_amount=AmountRangeTest.min_amount,
                                         max_amount=AmountRangeTest.max_amount)
        self.assertEqual(
            ar_obj.__str__(), str(self.ar_id)
        )

    def tearDown(self):
        """
        Truncate the Loan Table
        :return:
        """
        if self.db_name.startswith('test'):
            Loan.objects.all().delete()
            AmountRange.objects.all().delete()
