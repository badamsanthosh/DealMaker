from django.test import SimpleTestCase, Client
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
from rest_framework import status
from rest_framework_jwt.utils import jwt_encode_handler, api_settings
from dealmaker.libs.auth_utils import AuthUtil
from django.utils.timezone import localtime
from django.conf import settings
from django.test.client import RequestFactory
from datetime import datetime
from home_loans.views.home_loan_views import _p_and_i_estimate, _io_estimate, retrieve_cookie
from home_loans.models import Request, RequestCookieMap, Loan, AmountRange, LvrRange, Discount, Quote
from home_loans.models import ApplicableReason, ApplicableProperty, ApplicableState
from http.cookies import SimpleCookie
import time
import pdb

BASE_TOKEN = "wHi4l3g4iRcUHzQ25cg4Chu5OqryBL6y7PvHIFojAPCWStkROKGeKNPF0z4mobrn6YQZ/QDUwklKuBPZB4ULT2fvukF7Q8/" \
             "tomEl84daL3E+gThcpSWO+etMERq3vxLdIfc+DWo1Z8YlhiZ73AcszEuQNy/JQxcrQIv+EiKuQJydJm6Z1FYjC2OQL7LCbny" \
             "fUxTzoHXbYYjI56fNNtOwgY4tA2sFiv271xj+5DAU7zRt8FgSRZRW1/Iwvo/Lav5W0ZeIlp2oqH0SQ6Lmk1BI0y5uoRA0KC8" \
             "fsK0exvMaobd2VO0ttS1aXkB3T3HS4KAHBcuBgfuPiNfq2eZwMbzyjCQdN/jnq5w7KUlT0/8erkkqSoWDY4MS720uEqRv3KR" \
             "nfX2iNmEgRzVXzpi8ZkPjx1oFFHl99NGF+L8B9+E+J4BSDP6+BmUl3cl9Kj+JZl2l254vRmfi8uMY7Nj8jzEffkjiNINC+h" \
             "whQWwkCnmzoFjUlzzQ4WgdXw9VjKaJEhWbr5kPDIlbh/RamuHyigjU/meO/y0qw4P0WsS3qqqiLVs6vPHQQe7i1cG5B/Bhb" \
             "0UIvBgmaTADHBaLa2l0YmnILAzfXhyTOcXBrPOyKep63AkPBCF7rLs2CVwGf+zLzXd2TXNRe9lZqx+hL/gGpPwQ1poK3T35" \
             "S+ZqtsqT/ajvXKXC6/RtJrCPZQckXCXUibH9"


def generate_dummy_token():
    decrypted_token = AuthUtil.decrypt(BASE_TOKEN)
    payload_info = AuthUtil.get_payload(decrypted_token)
    payload_info['iat'] = time.mktime(localtime().timetuple())
    payload_info['exp'] = localtime() + api_settings.JWT_EXPIRATION_DELTA
    return AuthUtil.encrypt(jwt_encode_handler(payload_info)).decode("utf-8")


class HomeLoanAPITests(APITestCase):

    def test_request_create_without_cookie(self):
        request_data = {'first_name': 'RCT FName', 'last_name': 'RCT LName', 'channel_path': 'personal', 'state': 'VIC',
                        'postcode': '3250', 'amount': 600000, 'price': 750000, 'lvr': 75, 'disposable_income': 150000.0,
                        'show_fixed': True, 'show_variable': True, 'reason': 'buying', 'property_type': 'apartment',
                        'discarded': False}
        response = self.client.post(path='/home_loans/request/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_create_with_cookie(self):
        request_data = {'first_name': 'RCT FName', 'last_name': 'RCT LName', 'channel_path': 'personal', 'state': 'VIC',
                        'postcode': '3250', 'amount': 600000, 'price': 750000, 'lvr': 75, 'disposable_income': 150000.0,
                        'show_fixed': True, 'show_variable': True, 'reason': 'buying', 'property_type': 'apartment',
                        'discarded': False}
        self.client.cookies = SimpleCookie({'dpx': 'test'})
        response = self.client.post(path='/home_loans/request/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_create_with_exception(self):
        request_data = {'firstname': 'RCT FName', 'lastname': 'RCT LName', 'state': 'VIC',
                        'postcode': '3250', 'price': 750000, 'lvr': 75, 'disposable_income': 150000.0,
                        'show_fixed': True, 'show_variable': True, 'reason': 'buying', 'property_type': 'apartment',
                        'discarded': False}
        response = self.client.post(path='/home_loans/request/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_info_without_request_found(self):
        cookie_val = 'test'+datetime.now().strftime('%Y%m%d%H%s')
        self.client.cookies = SimpleCookie({'dpx': cookie_val})
        response = self.client.get(path='/home_loans/request/info/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_info_with_request_found(self):
        # Set up the requisite for test execution
        cookie_val = 'test'+datetime.now().strftime('%Y%m%d%H%s')
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='house',
                                            property_type='building')
        req_create.save()
        RequestCookieMap.objects.create(request_id=req_create, cookie=cookie_val).save()
        self.client.cookies = SimpleCookie({'dpx': cookie_val})
        response = self.client.get(path='/home_loans/request/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_price_request_view_retrieve(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='house',
                                            property_type='building')
        req_create.save()
        request_id = req_create.request_id
        path = "/home_loans/request_price/%d/" % request_id
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_price_smsf_request_view_retrieve(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='house',
                                            property_type='building')
        req_create.save()
        request_id = req_create.request_id
        path = "/home_loans/request_smsf_price/%d/" % request_id
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_quotes_no_request_found(self):
        request_data = {'request_id': -100}
        response = self.client.post(path='/home_loans/quote/generate_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_quotes_no_products_found(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='house',
                                            property_type='building')
        req_create.save()
        request_id = req_create.request_id
        request_data = {'request_id': request_id}
        response = self.client.post(path='/home_loans/quote/generate_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_quotes_no_request_id(self):
        response = self.client.post(path='/home_loans/quote/retrieve_quotes/', data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_quotes(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='house',
                                            property_type='building')
        req_create.save()
        request_id = req_create.request_id
        request_data = {'request_id': request_id}
        response = self.client.post(path='/home_loans/quote/retrieve_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_quotes_no_request_id(self):
        response = self.client.post(path='/home_loans/quote/request_quotes/', data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_quotes_no_quotes(self):
        request_data = {'request_id': -1}
        response = self.client.post(path='/home_loans/quote/request_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_total_quotes(self):
        response = self.client.get(path='/home_loans/quote/total_quotes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass


class QuotesAPITests(APITestCase):

    def setUp(self):
        pass

    def test_generate_quotes(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='investment',
                                            property_type='apartment')
        req_create.save()
        request_id = req_create.request_id
        request_data = {'request_id': request_id}
        add_new_loan(rate=3.48, cashback=1000)
        response = self.client.post(path='/home_loans/quote/generate_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Request.objects.all().delete()
        Loan.objects.all().delete()

    def test_generate_smsf_quotes(self):
        req_create = Request.objects.create(channel_path='smsf', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='investment',
                                            property_type='apartment')
        req_create.save()
        request_id = req_create.request_id
        request_data = {'request_id': request_id}
        add_new_loan(rate=3.48, cashback=1000, channel_path='smsf')
        response = self.client.post(path='/home_loans/quote/generate_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        Request.objects.all().delete()
        Loan.objects.all().delete()
        Quote.objects.all().delete()

    def test_request_quotes_with_data(self):
        req_create = Request.objects.create(channel_path='personal', state='VIC', postcode='3000', amount=500000,
                                            price=300000, lvr=80, disposable_income=150000, reason='investment',
                                            property_type='apartment')
        req_create.save()
        request_id = req_create.request_id
        request_data = {'request_id': request_id}
        add_new_loan(rate=3.68, cashback=1000)
        self.client.post(path='/home_loans/quote/generate_quotes/', data=request_data, format='json')
        response = self.client.post(path='/home_loans/quote/request_quotes/', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Request.objects.all().delete()
        Loan.objects.all().delete()
        Quote.objects.all().delete()

    def tearDown(self):
        pass


class LoanViewSetTest(APITransactionTestCase):

    def test_create_loan(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_update_loan(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))
        url = '/home_loans/loan/'+loan_id+'/'

        # Update Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_update_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "3.20"
        }
        response = client.put(path=url, data=loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_retrieve_loan(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))
        url = '/home_loans/loan/'+loan_id+'/'

        response = client.get(path=url, data=loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_list_loan(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        client.post(path='/home_loans/loan/', data=loan_data, format='json')

        response = client.get(path='/home_loans/loan/', data=loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_delete_loan(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))
        url = '/home_loans/loan/'+loan_id+'/'

        response = client.delete(path=url, data=loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        Loan.objects.filter(product_name__startswith='test').delete()


class AmountRangeViewSetTest(APITransactionTestCase):

    def test_create_amount_range(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "3.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = response.data.get('loan_id')

        data = {
            "min_amount": 100000,
            "max_amount": 2000000,
            "loan_id": loan_id
        }
        response = client.post(path='/home_loans/amount_range/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_update_amount_range(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))

        data = {
            "min_amount": 100000,
            "max_amount": 2000000,
            "loan_id": loan_id
        }
        response = client.post(path='/home_loans/amount_range/', data=data, format='json')
        amount_range_id = str(response.data.get('amount_range_id'))
        url = '/home_loans/amount_range/'+amount_range_id+'/'

        # Update Brand
        amount_range_data = {
            "min_amount": 120000,
            "max_amount": 2500000,
            "loan_id": loan_id
        }
        response = client.put(path=url, data=amount_range_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_retrieve_amount_range(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))

        data = {
            "min_amount": 100000,
            "max_amount": 2000000,
            "loan_id": loan_id
        }
        response = client.post(path='/home_loans/amount_range/', data=data, format='json')
        amount_range_id = str(response.data.get('amount_range_id'))
        url = '/home_loans/amount_range/'+amount_range_id+'/'

        response = client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_list_amount_range(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))

        data = {
            "min_amount": 100000,
            "max_amount": 2000000,
            "loan_id": loan_id
        }
        client.post(path='/home_loans/amount_range/', data=data, format='json')

        response = client.get(path='/home_loans/amount_range/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_delete_amount_range(self):
        Loan.objects.filter(product_name__startswith='test').delete()
        token = generate_dummy_token()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # Create Brand
        loan_data = {
            "frequencies": [
                "weekly",
                "monthly",
                "fortnightly"
            ],
            "product_name": "test_Loan",
            "brand_name": "Bank of Melbourne",
            "channel_path": "personal",
            "owner_id": 1,
            "brand_path": "bom",
            "rate_type": "fixed",
            "rate": "5.20"
        }
        response = client.post(path='/home_loans/loan/', data=loan_data, format='json')
        loan_id = str(response.data.get('loan_id'))

        data = {
            "min_amount": 100000,
            "max_amount": 2000000,
            "loan_id": loan_id
        }
        response = client.post(path='/home_loans/amount_range/', data=data, format='json')
        amount_range_id = str(response.data.get('amount_range_id'))
        url = '/home_loans/amount_range/'+amount_range_id+'/'

        response = client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        Loan.objects.filter(product_name__startswith='test').delete()


class LVRRangeViewSetTest(APITransactionTestCase):

    def setUp(self):
        token = generate_dummy_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_create_lvr_range(self):
        loan_id = create_loan()

        data = {
            "min_lvr": 0,
            "max_lvr": 95,
            "loan_id": loan_id
        }
        response = self.client.post(path='/home_loans/lvr_range/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lvr_range(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        url = '/home_loans/lvr_range/'+str(lvr_range_id)+'/'

        # Update LVR Range
        lvr_range_data = {
            "min_lvr": 0,
            "max_lvr": 90,
            "loan_id": loan_id
        }
        response = self.client.put(path=url, data=lvr_range_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lvr_range(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        url = '/home_loans/lvr_range/'+str(lvr_range_id)+'/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lvr_range(self):
        loan_id = create_loan()
        create_lvr_range(loan_id)
        response = self.client.get(path='/home_loans/lvr_range/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lvr_range(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        url = '/home_loans/lvr_range/'+str(lvr_range_id)+'/'
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Loan.objects.filter(product_name__startswith='test').delete()


class ApplicablePropertyViewSetTest(APITransactionTestCase):

    def setUp(self):
        token = generate_dummy_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_create(self):
        loan_id = create_loan()
        data = [
            {
                "property_type": "apartment",
                "loan_id": loan_id
            },
            {
                "property_type": "house",
                "loan_id": loan_id
            }
        ]
        response = self.client.post(path='/home_loans/loan_property/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_exception(self):
        data = [
            {
                "property_type": "apartment",
                "loan_id": -1
            }
        ]
        response = self.client.post(path='/home_loans/loan_property/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        loan_id = create_loan()
        applies_to_property_type_id = create_applicable_property(loan_id)
        url = '/home_loans/loan_property/'+str(applies_to_property_type_id)+'/'
        data = {
            "property_type": "test_prop",
            "loan_id": loan_id
        }
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        loan_id = create_loan()
        applies_to_property_type_id = create_applicable_property(loan_id)
        url = '/home_loans/loan_property/'+str(applies_to_property_type_id)+'/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        loan_id = create_loan()
        create_applicable_property(loan_id)
        response = self.client.get(path='/home_loans/loan_property/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        loan_id = create_loan()
        applies_to_property_type_id = create_applicable_property(loan_id)
        url = '/home_loans/loan_property/'+str(applies_to_property_type_id)+'/'
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Loan.objects.filter(product_name__startswith='test').delete()


class ApplicableReasonViewSetTest(APITransactionTestCase):

    def setUp(self):
        token = generate_dummy_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_create(self):
        loan_id = create_loan()
        data = [
            {
                "reason": "first_home_buyer",
                "loan_id": loan_id
            },
            {
                "reason": "investment",
                "loan_id": loan_id
            }
        ]
        response = self.client.post(path='/home_loans/loan_reason/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_exception(self):
        data = [
            {
                "reason": "test_reason",
                "loan_id": -1
            }
        ]
        response = self.client.post(path='/home_loans/loan_reason/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        loan_id = create_loan()
        applies_to_reason_id = create_applicable_reason(loan_id)
        url = '/home_loans/loan_reason/'+str(applies_to_reason_id)+'/'
        data = {
            "reason": "test_reason_update",
            "loan_id": loan_id
        }
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        loan_id = create_loan()
        applies_to_reason_id = create_applicable_reason(loan_id)
        url = '/home_loans/loan_reason/'+str(applies_to_reason_id)+'/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        loan_id = create_loan()
        create_applicable_reason(loan_id)
        response = self.client.get(path='/home_loans/loan_reason/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        loan_id = create_loan()
        applies_to_reason_id = create_applicable_reason(loan_id)
        url = '/home_loans/loan_reason/'+str(applies_to_reason_id)+'/'
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Loan.objects.filter(product_name__startswith='test').delete()


class ApplicableStateViewSetTest(APITransactionTestCase):

    def setUp(self):
        token = generate_dummy_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_create(self):
        loan_id = create_loan()
        data = [
            {
                "state": "ACT",
                "loan_id": loan_id
            },
            {
                "state": "NSW",
                "loan_id": loan_id
            }
        ]
        response = self.client.post(path='/home_loans/loan_state/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_exception(self):
        data = [
            {
                "state": "test_state",
                "loan_id": -1
            }
        ]
        response = self.client.post(path='/home_loans/loan_state/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        loan_id = create_loan()
        applies_to_state_id = create_applicable_state(loan_id)
        url = '/home_loans/loan_state/'+str(applies_to_state_id)+'/'
        data = {
            "state": "test_state",
            "loan_id": loan_id
        }
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        loan_id = create_loan()
        applies_to_state_id = create_applicable_state(loan_id)
        url = '/home_loans/loan_state/'+str(applies_to_state_id)+'/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        loan_id = create_loan()
        create_applicable_state(loan_id)
        response = self.client.get(path='/home_loans/loan_state/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        loan_id = create_loan()
        applies_to_state_id = create_applicable_state(loan_id)
        url = '/home_loans/loan_state/'+str(applies_to_state_id)+'/'
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Loan.objects.filter(product_name__startswith='test').delete()


class DiscountViewSetTest(APITransactionTestCase):

    def setUp(self):
        token = generate_dummy_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        Loan.objects.filter(product_name__startswith='test').delete()

    def test_discount_create(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        amount_range_id = create_amount_range(loan_id)
        data = {
            "rate": "0.12",
            "loan_id": loan_id,
            "lvr_range_id": lvr_range_id,
            "amount_range_id": amount_range_id
        }
        response = self.client.post(path='/home_loans/discount/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_discount_update(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        amount_range_id = create_amount_range(loan_id)
        discount_id = create_discount(loan_id, lvr_range_id, amount_range_id)
        url = '/home_loans/discount/'+str(discount_id)+'/'
        data = {
            "rate": "0.10",
            "loan_id": loan_id,
            "lvr_range_id": lvr_range_id,
            "amount_range_id": amount_range_id
        }
        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_retrieve(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        amount_range_id = create_amount_range(loan_id)
        discount_id = create_discount(loan_id, lvr_range_id, amount_range_id)
        url = '/home_loans/discount/'+str(discount_id)+'/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_list(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        amount_range_id = create_amount_range(loan_id)
        create_discount(loan_id, lvr_range_id, amount_range_id)
        url = '/home_loans/discount/'
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_delete(self):
        loan_id = create_loan()
        lvr_range_id = create_lvr_range(loan_id)
        amount_range_id = create_amount_range(loan_id)
        discount_id = create_discount(loan_id, lvr_range_id, amount_range_id)
        url = '/home_loans/discount/'+str(discount_id)+'/'
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        Loan.objects.filter(product_name__startswith='test').delete()


def create_loan():
    loan_obj = Loan(
        product_name="test_Loan",
        brand_name="Bank of Melbourne",
        channel_path="personal",
        owner_id=1,
        brand_path="bom",
        rate_type="fixed",
        rate="5.20",
        frequencies='{weekly,monthly,fortnightly}'
    )
    loan_obj.save()
    return loan_obj.loan_id


def create_lvr_range(loan_id):
    lvr_obj = LvrRange(
        min_lvr=0,
        max_lvr=95,
        loan_id=Loan.objects.get(loan_id=loan_id)
    )
    lvr_obj.save()
    return lvr_obj.lvr_range_id


def create_amount_range(loan_id):
    amt_range_obj = AmountRange(
        min_amount=100000,
        max_amount=2000000,
        loan_id=Loan.objects.get(loan_id=loan_id)
    )
    amt_range_obj.save()
    return amt_range_obj.amount_range_id


def create_discount(loan_id, lvr_range_id, amount_range_id):
    discount_obj = Discount(
        loan_id=Loan.objects.get(loan_id=loan_id),
        lvr_range_id=LvrRange.objects.get(lvr_range_id=lvr_range_id),
        amount_range_id=AmountRange.objects.get(amount_range_id=amount_range_id),
        rate="0.15"
    )
    discount_obj.save()
    return discount_obj.discount_id


def create_applicable_property(loan_id):
    app_prop_obj = ApplicableProperty(
        property_type="apartment",
        loan_id=Loan.objects.get(loan_id=loan_id)
    )
    app_prop_obj.save()
    return app_prop_obj.applies_to_property_type_id


def create_applicable_reason(loan_id):
    app_reason_obj = ApplicableReason(
        reason="apartment",
        loan_id=Loan.objects.get(loan_id=loan_id)
    )
    app_reason_obj.save()
    return app_reason_obj.applies_to_reason_id


def create_applicable_state(loan_id):
    app_state_obj = ApplicableState(
        state="ACT",
        loan_id=Loan.objects.get(loan_id=loan_id)
    )
    app_state_obj.save()
    return app_state_obj.applies_to_state_id


class HomeLoanViewTests(SimpleTestCase):

    def setUp(self):
        self.req_factory = RequestFactory()

    """
    Unit TestCases for Helper functions
    """

    def test_p_and_i_estimate(self):
        rate = 3.5
        amount = 300000

        # TestCase where divisor value is > 1
        self.assertEqual(
            _p_and_i_estimate(rate, amount), 1347
        )
        # TestCase where divisor value is < 1
        self.assertEqual(
            _p_and_i_estimate(rate, amount, num_years=-10), 0
        )

        # TestCase with Exception
        self.assertEqual(
            _p_and_i_estimate(rate, amount='300000'), 0
        )

    def test_io_estimate(self):
        rate = 3.5
        amount = 300000

        # TestCase with float/integer
        self.assertEqual(
            _io_estimate(rate, amount), 875
        )

        # TestCase with input containing string
        self.assertEqual(
            _io_estimate(rate, amount='300000'), 0
        )

    """
    Unit TestCases for Cookie ViewSet
    """

    def test_retrieve_cookie(self):
        req_fact = self.req_factory.get('/home_loans/cookie/set_cookie/')
        req_fact.COOKIES['dpx'] = 'test-cookie'
        self.assertEqual(
            retrieve_cookie(req_fact), 'test-cookie'
        )

    def test_set_cookie(self):
        client = Client()
        resp = client.get('/home_loans/cookie/set_cookie/')
        self.assertIn(
            "dpx", resp.cookies.keys()
        )
        self.assertEqual(
            len(resp.cookies.get('dpx').value), 36
        )

    def test_set_with_existing_cookie(self):
        client = Client()
        resp = client.get('/home_loans/cookie/set_cookie/')
        self.assertIn(
            "dpx", resp.cookies.keys()
        )
        resp = client.get('/home_loans/cookie/set_cookie/')
        self.assertEqual(
            len(resp.data['cookie']['dpx']), 36
        )

    def test_get_cookie(self):
        cookie = SimpleCookie()
        cookie["dpx"] = "test-cookie"
        expected_api_resp = "Cookie is successfully set to {'dpx': 'test-cookie'}"
        client = Client(HTTP_COOKIE=cookie.output(header='', sep='; '))
        resp = client.get('/home_loans/cookie/get_cookie/')
        self.assertEqual(
            resp.data, expected_api_resp
        )
        self.assertEqual(
            resp.status_code, 200
        )

    def tearDown(self):
        pass


def add_new_loan(rate=3.66, cashback=1250, channel_path='personal'):
    loan_obj = Loan.objects.create(
        product_name='Standard Fixed (P & I) - Owner Occupied',
        brand_name='Bank of Queensland',
        is_attached=True,
        is_current=True,
        channel_path=channel_path,
        brand_path='bmq',
        display_name='Standard Fixed 1 Year',
        description='Standard Fixed (P & I) - Owner Occupied',
        rate_type='fixed',
        fixed_term=1,
        owner_id=1,
        min_amount=100000,
        max_amount=9999999,
        max_lvr=95,
        rate=rate,
        has_cashback=True,
        has_postcode_discount=True,
        cashback=cashback,
        frequencies='{"weekly","fortnightly", "monthly"}',
    )
    loan_obj.save()
    loan_id = loan_obj.loan_id

    amt_range_1 = AmountRange.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        min_amount=30000,
        max_amount=199999
    )
    amt_range_1.save()
    amt_id_1 = amt_range_1.amount_range_id

    amt_range_2 = AmountRange.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        min_amount=200000,
        max_amount=2000000
    )
    amt_range_2.save()
    amt_id_2 = amt_range_2.amount_range_id

    lvr_range_1 = LvrRange.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        min_lvr=0,
        max_lvr=80
    )
    lvr_range_1.save()
    lvr_1 = lvr_range_1.lvr_range_id

    lvr_range_2 = LvrRange.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        min_lvr=81,
        max_lvr=90
    )
    lvr_range_2.save()
    lvr_2 = lvr_range_2.lvr_range_id

    disc_1 = Discount.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        amount_range_id=AmountRange.objects.get(amount_range_id=amt_id_1),
        lvr_range_id=LvrRange.objects.get(lvr_range_id=lvr_1),
        rate=0.14,
    )
    disc_1.save()

    disc_2 = Discount.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        amount_range_id=AmountRange.objects.get(amount_range_id=amt_id_2),
        lvr_range_id=LvrRange.objects.get(lvr_range_id=lvr_2),
        rate=0.04,
    )
    disc_2.save()

    ap_1 = ApplicableProperty.objects.create(
        property_type='apartment',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ap_1.save()

    ap_2 = ApplicableProperty.objects.create(
        property_type='house',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ap_2.save()

    ap_3 = ApplicableProperty.objects.create(
        property_type='land',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ap_3.save()

    ar_1 = ApplicableReason.objects.create(
        reason='first_home_buyer',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ar_1.save()

    ar_2 = ApplicableReason.objects.create(
        reason='investment',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ar_2.save()

    ar_3 = ApplicableReason.objects.create(
        reason='refinance_investment',
        loan_id=Loan.objects.get(loan_id=loan_id),
    )
    ar_3.save()

    as_1 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='ACT',
    )
    as_1.save()

    as_2 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='NSW',
    )
    as_2.save()

    as_3 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='NT',
    )
    as_3.save()

    as_4 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='QLD',
    )
    as_4.save()

    as_5 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='SA',
    )
    as_5.save()

    as_6 = ApplicableState.objects.create(
        loan_id=Loan.objects.get(loan_id=loan_id),
        state='VIC',
    )
    as_6.save()
