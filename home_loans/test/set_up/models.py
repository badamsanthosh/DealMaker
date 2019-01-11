from home_loans.models import Loan, Quote, Request


"""
Add a Test Home Home Loan
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

loan_obj = Loan(product_name=product_name, brand_name=brand_name, channel_path=channel_path, owner_id=owner_id,
                brand_path=brand_path, display_name=display_name, description=description, rate_type=rate_type,
                fixed_term=fixed_term, min_amount=min_amount, max_amount=max_amount, max_lvr=max_lvr, rate=rate,
                frequencies=frequencies)
loan_obj.save()

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

loan_obj = Loan(product_name=product_name, brand_name=brand_name, channel_path=channel_path, owner_id=owner_id,
                brand_path=brand_path, display_name=display_name, description=description, rate_type=rate_type,
                fixed_term=fixed_term, min_amount=min_amount, max_amount=max_amount, max_lvr=max_lvr, rate=rate,
                frequencies=frequencies)
loan_obj.save()


brand_name = "Bank of Melbourne"
request_id = Request.objects.get(request_id=3)
product_name = "Simply Loan"
p_and_i_estimate = 50
io_estimate = 75
rate = 3.45
advertised_rate = 3.65
rate_type = "fixed"
max_lvr = 90
min_amount = 9999
max_amount = 99999999
has_offset = True
has_redraw = True
has_extra_payments = False
has_extra_payment_penalty = False
has_interest_only = False
frequencies = ["Weekly", "Fortnightly", "Monthly"]
application_fee = 2500.00
description = "Test Desc"
brand_path = "bom"
is_current = True
request_attempt = 1
quote_obj = Quote(request_id=request_id, brand_name=brand_name, product_name=product_name,
                  p_and_i_estimate=p_and_i_estimate, io_estimate=io_estimate, rate=rate,
                  advertised_rate=advertised_rate, rate_type=rate_type,
                  max_lvr=max_lvr, min_amount=min_amount, max_amount=max_amount, has_offset=has_offset,
                  has_redraw=has_redraw, has_extra_payments=has_extra_payments,
                  has_extra_payment_penalty=has_extra_payment_penalty, has_interest_only=has_interest_only,
                  frequencies=frequencies, application_fee=application_fee, description=description,
                  brand_path=brand_path, is_current=True, request_attempt=request_attempt)
quote_obj.save()
