from home_loans.models.base_model import BaseModel
from home_loans.models.home_loan_models import Loan, Request, Discount
from home_loans.models.home_loan_models import RequestNote, Quote, RequestCookieMap, RequestArchive
from home_loans.models.home_loan_models import AmountRange, LvrRange, ApplicableProperty, ApplicableReason, ApplicableState
from home_loans.models.db_view_models import PriceRequestView, PriceSMSFRequestView, SimilarRequestView, QuotesView



class Meta:
    app_label = 'home_loans'
