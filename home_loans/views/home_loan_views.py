import datetime
import pandas as pd
import numpy as np

# Import Rest Framework modules
from rest_framework import viewsets, mixins, status
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Value, BooleanField
from rest_framework.decorators import action
from rest_framework.response import Response

# Import Serializers
from home_loans.serializers import LoanSerializer, RequestSerializer
from home_loans.serializers import PriceRequestViewSerializer, PriceSMSFRequestViewSerializer, QuoteSerializer, \
    RequestCookieMapSerializer, QuotesViewSerializer, AmountRangeSerializer, LvrRangeSerializer, DiscountSerializer
from home_loans.serializers import ApplicablePropertySerializer, ApplicableStateSerializer, ApplicableReasonSerializer

# Import Models for ModelViewSets
from home_loans.models import PriceRequestView, PriceSMSFRequestView, RequestCookieMap, QuotesView, AmountRange
from home_loans.models import ApplicableState, ApplicableReason, ApplicableProperty
from home_loans.models import LvrRange, Discount
from home_loans.constants import SMSF_MATCHING_STR
from home_loans.constants import FROM_DELETED_BRANDS_1, FROM_DELETED_BRANDS_2, FROM_RATE_CITY, OLD_TD_CATEGORY
from home_loans.models import Loan, Request, Quote

from dealmaker.libs.dpx_logger import DpxLogger
from utils.dmx_exception_handler import custom_drf_exception
from utils.generics import Generics
from dealmaker import dpx_authenticator
from utils.permissions import is_authorized

# Import Task for Async jobs
from home_loans.tasks import salesforce_sync


"""
******************************************************************************
***************************** Model ViewSets *********************************
******************************************************************************
"""


class LoanViewSet(viewsets.ModelViewSet):
    """
    Loan ViewSet to manage loan object
    """
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AmountRangeViewSet(viewsets.ModelViewSet):
    """
    Amount range ViewSet to manage loan object
    """
    serializer_class = AmountRangeSerializer
    queryset = AmountRange.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LVRRangeViewSet(viewsets.ModelViewSet):
    """
    LVR range ViewSet to manage loan object
    """
    serializer_class = LvrRangeSerializer
    queryset = LvrRange.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DiscountViewSet(viewsets.ModelViewSet):
    """
    Discount range ViewSet to manage loan object
    """
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ApplicablePropertyViewSet(viewsets.ModelViewSet):
    """
    Applicable Property range ViewSet to manage loan object
    """
    serializer_class = ApplicablePropertySerializer
    queryset = ApplicableProperty.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        try:
            serializer = ApplicablePropertySerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ApplicableReasonViewSet(viewsets.ModelViewSet):
    """
    Applicable Property range ViewSet to manage loan object
    """
    serializer_class = ApplicableReasonSerializer
    queryset = ApplicableReason.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        try:
            serializer = ApplicableReasonSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ApplicableStateViewSet(viewsets.ModelViewSet):
    """
    Applicable Property range ViewSet to manage loan object
    """
    serializer_class = ApplicableStateSerializer
    queryset = ApplicableState.objects.all()

    @dpx_authenticator
    @is_authorized('home_loans')
    def create(self, request, *args, **kwargs):
        try:
            serializer = ApplicableStateSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @dpx_authenticator
    @is_authorized('home_loans')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @dpx_authenticator
    @is_authorized('home_loans')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RequestViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    Request ViewSet: Manage Home loan requests
    """
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            DpxLogger.get_logger().info("Creating New Request")
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            request_id = serializer.save().request_id

            # Insert record into RequestCookieMap table
            cookie = retrieve_cookie(request)
            if cookie:
                req_cookie_data = {'request_id': request_id, 'cookie': cookie}
                serializer_rc = RequestCookieMapSerializer(data=req_cookie_data)
                serializer_rc.is_valid(raise_exception=True)
                serializer_rc.save()

            lead_info = data
            lead_info['created_on'] = serializer.data.get('created_on')
            salesforce_sync.delay(lead_info=data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as exc:
            return custom_drf_exception(exc, context={'request': request})

    @action(methods=['GET'], detail=False)
    def info(self, request):
        """
        :param request: Get cookie from request parameter
        :return: Returns request object information.
        """
        cookie = retrieve_cookie(request)
        filtered_request = RequestCookieMap.objects.filter(cookie=cookie).order_by('-request_id')
        if filtered_request:
            request_id = RequestCookieMap.objects.filter(cookie=cookie).order_by('-request_id')[0].request_id_id
        else:
            return Response("No Requests found", status=status.HTTP_204_NO_CONTENT)
        req_obj = Request.objects.get(request_id=request_id)
        serializer = RequestSerializer(req_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
******************************************************************************
***************************** Business ViewSets ******************************
******************************************************************************
"""


class PriceRequestViewSet(viewsets.ViewSet):
    """
    Price Request View:
     - This is view gets the data from home loans database view - "price_request_view"
    """

    def retrieve(self, request, request_id):
        request_price = PriceRequestView.objects.filter(request_id=request_id)
        serializer = PriceRequestViewSerializer(request_price, many=True)
        return Response(serializer.data)


class PriceSMSFRequestViewSet(viewsets.ViewSet):
    """
    Price SMSF Request View:
        - This is view gets the data from home loans database view - "price_smsf_request_view"
    """

    def retrieve(self, request, request_id):
        request_price = PriceSMSFRequestView.objects.filter(request_id=request_id)
        serializer = PriceSMSFRequestViewSerializer(request_price, many=True)
        return Response(serializer.data)


class QuoteViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    def generate_quotes(self, request):
        """
        :param request: request_id post parameter
        :return: Response

        API to populate generate quotes for a given Request ID.
        Steps:
            1. Get amount and channel path for request id.
            2. Get price information from concerned view based on the channel path
            3. Serialize the data from Quote Serializer.
            4. Delete existing quotes for the request id.
            5. Push the newly generated quotes in the Quotes table.
        """
        request_id = request.data.get('request_id')
        filtered_request = Request.objects.filter(request_id=request_id).values('amount', 'channel_path')
        if not filtered_request:
            return Response("RequestID not found", status=status.HTTP_400_BAD_REQUEST)
        req_obj = filtered_request[0]
        channel_path = req_obj.get('channel_path')
        amount = req_obj.get('amount')
        if SMSF_MATCHING_STR in channel_path:
            prices_info = "PriceSMSFRequestView"
        else:
            prices_info = "PriceRequestView"

        # Get Product Prices Information
        prices_obj = eval(prices_info).objects.filter(request_id=request_id)
        if not prices_obj:
            return Response("No products found for given request", status=status.HTTP_204_NO_CONTENT)

        # Prepare DataFrame for the price object.
        prices_df = pd.DataFrame(
            list(
                    prices_obj.values(
                        'request_id', 'loan_id', 'rate', 'cashback'
                    ).annotate(
                        is_current=Value(True, BooleanField())
                    )
                )
        )
        prices_df['p_and_i_estimate'] = np.vectorize(_p_and_i_estimate)(
            prices_df['rate'], amount
        )
        prices_df['io_estimate'] = np.vectorize(_io_estimate)(
            prices_df['rate'], amount
        )

        Quote.objects.filter(request_id=request_id).update(is_current=False)
        serializer = QuoteSerializer(data=prices_df.to_dict(orient='records'), many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def retrieve_quotes(self, request):
        request_id = request.data.get('request_id')
        if not request_id:
            return Response("Please provide valid request id", status=status.HTTP_400_BAD_REQUEST)
        quotes = QuotesView.objects.filter(request_id=request_id)
        serializer = QuotesViewSerializer(quotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def request_quotes(self, request):
        request_id = request.data.get('request_id')
        if not request_id:
            return Response("Please provide valid request id", status=status.HTTP_400_BAD_REQUEST)
        quotes_obj = QuotesView.objects.filter(request_id=request_id)
        if not quotes_obj:
            return Response("No quotes found for given request", status=status.HTTP_204_NO_CONTENT)
        quotes_df = pd.DataFrame(
            list(
                quotes_obj.values(
                    'brand_name', 'rate'
                )
            )
        )
        brands_list = quotes_df.brand_name.unique().tolist()
        request_quotes = dict()
        request_quotes['num_brands'] = len(brands_list)
        request_quotes['best_rate'] = quotes_df['rate'].min()
        request_quotes['num_quotes'] = len(quotes_df)
        request_quotes['brands_list'] = brands_list
        return Response(request_quotes, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def total_quotes(self, request):
        db_quotes_count = Quote.objects.all().count()
        total_quotes = db_quotes_count+OLD_TD_CATEGORY+FROM_DELETED_BRANDS_1+FROM_DELETED_BRANDS_2+FROM_RATE_CITY
        response_dict = dict()
        response_dict['total_quotes'] = total_quotes
        return Response(response_dict, status=status.HTTP_200_OK)


class CookieViewSet(viewsets.ViewSet):

    @action(methods=['GET'], detail=False)
    def set_cookie(self, request):
        response = HttpResponse("Setting dp.exchange cookie")
        if request.COOKIES:
            existing_cookie = {"cookie": request.COOKIES}
            return Response(existing_cookie, status=status.HTTP_200_OK)
        cookie = Generics.generate_cookie()
        max_age = settings.COOKIE_MAX_AGE or 365 * 24 * 60 * 60
        key = settings.COOKIE_KEY
        # domain = settings.COOKIE_DOMAIN
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                                             datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key=key, value=cookie, expires=expires, max_age=max_age)
        return response

    @action(methods=['GET'], detail=False)
    def get_cookie(self, request):
        cookie_data = request.COOKIES
        response_data = "Cookie is successfully set to %s" % cookie_data
        return Response(response_data, status=status.HTTP_200_OK)


"""
*********************************************************************************************
******************************** Home Loan App Specific functions ***************************
*********************************************************************************************
"""


def retrieve_cookie(request_obj):
    return request_obj.COOKIES.get('dpx') or ''


def _p_and_i_estimate(rate, amount, num_years=30):
    try:
        divisor = 1 - (1+rate/(100 * 12))**(-num_years*12)
        if divisor > 0:
            return int(
                amount
                * (rate/(100*12))
                / divisor
            )
        return 0

    except Exception as exc:
        return 0


def _io_estimate(rate, amount):
    try:
        return int(
            amount
            * rate
            / (100*12)
        )

    except Exception as exc:
        return 0
