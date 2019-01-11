from rest_framework import routers
from django.urls import re_path
from home_loans.views import LoanViewSet, RequestViewSet, QuoteViewSet, PriceRequestViewSet, PriceSMSFRequestViewSet
from home_loans.views import AmountRangeViewSet, LVRRangeViewSet, DiscountViewSet
from home_loans.views import ApplicablePropertyViewSet, ApplicableReasonViewSet, ApplicableStateViewSet
from home_loans.views import CookieViewSet

router = routers.SimpleRouter()
router.register(r'loan', LoanViewSet, base_name='loan')
router.register(r'loan_property', ApplicablePropertyViewSet, base_name='loan_property')
router.register(r'loan_reason', ApplicableReasonViewSet, base_name='loan_reason')
router.register(r'loan_state', ApplicableStateViewSet, base_name='loan_state')
router.register(r'amount_range', AmountRangeViewSet, base_name='amount_range')
router.register(r'lvr_range', LVRRangeViewSet, base_name='lvr_range')
router.register(r'discount', DiscountViewSet, base_name='discount')
router.register(r'request', RequestViewSet, base_name='request')
router.register(r'quote', QuoteViewSet, base_name='quote')
router.register(r'cookie', CookieViewSet, base_name='cookie')


urlpatterns = [
        re_path(r'^request_price/(?P<request_id>[^/.]+)/$', PriceRequestViewSet.as_view({'get': 'retrieve'})),
        re_path(r'^request_smsf_price/(?P<request_id>[^/.]+)/$', PriceSMSFRequestViewSet.as_view({'get': 'retrieve'})),
    ]

urlpatterns += router.urls
