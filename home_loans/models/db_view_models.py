from django.db import models
from django.contrib.postgres.fields import ArrayField


class PriceRequestView(models.Model):
    request_id = models.IntegerField(primary_key=True)
    loan_id = models.IntegerField()
    brand_path = models.CharField(blank=False, null=False, max_length=75)
    rate_type = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    cashback = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"price_request_view'
        managed = False

    def __str__(self):
        """
        :return:  Returns the Request ID
        """
        return str(self.request_id)


class PriceSMSFRequestView(models.Model):
    request_id = models.IntegerField(primary_key=True)
    loan_id = models.IntegerField()
    brand_path = models.CharField(blank=False, null=False, max_length=75)
    rate_type = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    cashback = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"price_smsf_request_view'
        managed = False

    def __str__(self):
        """
        :return:  Returns the Request ID
        """
        return str(self.request_id)


class SimilarRequestView(models.Model):
    request_id = models.IntegerField(primary_key=True)
    similar_request_id = models.IntegerField()
    created_on = models.DateTimeField()
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    amount = models.IntegerField()

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"similar_view'
        managed = False

    def __str__(self):
        """
        :return:  Returns the Request ID
        """
        return str(self.request_id)


class QuotesView(models.Model):
    quote_id = models.IntegerField(primary_key=True)
    request_id = models.IntegerField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    cashback = models.IntegerField(blank=True, null=True)
    p_and_i_estimate = models.IntegerField(blank=True, null=True)
    io_estimate = models.IntegerField(blank=True, null=True)
    brand_path = models.CharField(blank=False, null=False, max_length=75)
    brand_name = models.CharField(blank=False, null=False, max_length=75)
    name = models.CharField(blank=False, null=True, max_length=125)
    description = models.CharField(blank=False, null=True, max_length=150)
    is_honeymoon = models.NullBooleanField()
    advertised_rate = models.DecimalField(max_digits=5, decimal_places=2)
    rate_type = models.CharField(max_length=50)
    fixed_term = models.IntegerField(blank=True, null=True)
    max_term = models.IntegerField(blank=True, null=True)
    max_lvr = models.IntegerField(blank=True, null=True)
    min_amount = models.IntegerField(blank=True, null=True)
    max_amount = models.IntegerField(blank=True, null=True)
    has_offset = models.NullBooleanField()
    has_redraw = models.NullBooleanField()
    has_extra_payments = models.NullBooleanField()
    has_extra_payment_penalty = models.NullBooleanField()
    has_interest_only = models.NullBooleanField()
    frequencies = ArrayField(models.CharField(blank=False, null=False, max_length=50))
    application_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    annual_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    max_rent_towards_repayment = models.IntegerField(blank=True, null=True)
    max_super_towards_repayment = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"quote_view'
        managed = False

    def __str__(self):
        """
        :return:  Returns the Quote ID
        """
        return str(self.quote_id)
