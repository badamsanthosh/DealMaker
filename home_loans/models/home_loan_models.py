from django.db import models
from home_loans.models.base_model import BaseModel
from django.contrib.postgres.fields import ArrayField


class Loan(BaseModel):

    CHANNEL_PATH_CHOICES = (
        ('personal', 'personal'),
        ('business', 'business'),
        ('commercial', 'commercial'),
        ('smsf', 'smsf'),
        ('low_doc', 'low_doc'),
    )
    RATE_TYPE_CHOICES = (
        ('fixed', 'fixed'),
        ('variable', 'variable'),
    )

    loan_id = models.AutoField(primary_key=True)
    product_name = models.CharField(blank=False, null=False, max_length=125)
    brand_name = models.CharField(blank=False, null=False, max_length=75)
    is_attached = models.BooleanField(default=False)
    is_current = models.BooleanField(default=False)
    parent_id = models.IntegerField(blank=True, null=True)
    channel_path = models.CharField(max_length=75)
    owner_id = models.IntegerField()
    brand_path = models.CharField(blank=False, null=False, max_length=75)
    display_name = models.CharField(blank=False, null=True, max_length=125)
    description = models.CharField(blank=False, null=True, max_length=150)
    rate_type = models.CharField(max_length=50)
    fixed_term = models.IntegerField(blank=True, null=True)
    min_amount = models.IntegerField(blank=True, null=True)
    max_amount = models.IntegerField(blank=True, null=True)
    max_lvr = models.IntegerField(blank=True, null=True)
    trustee_must_be_a_company = models.NullBooleanField()
    min_trust_balance = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    has_cashback = models.NullBooleanField()
    has_postcode_discount = models.NullBooleanField()
    has_value_discounts = models.NullBooleanField()
    is_honeymoon = models.NullBooleanField()
    cashback = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    cashback_is_a_rate = models.NullBooleanField()
    cashback_legal = models.NullBooleanField()
    postcode_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    postcode_discount_list_id = models.IntegerField(null=True, blank=True)
    postcode_exclusion_list_id = models.IntegerField(null=True, blank=True)
    max_term = models.IntegerField(blank=True, null=True)
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
        db_table = 'home_loans\".\"loan'
        ordering = ['-created_on']

    def __str__(self):
        """
        :return:  Returns the home loan product name
        """
        return self.product_name


class AmountRange(BaseModel):
    amount_range_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    min_amount = models.IntegerField()
    max_amount = models.IntegerField()

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"amount_range'
        unique_together = ("loan_id", "min_amount", "max_amount")

    def __str__(self):
        """
        :return: Returns the amount range id
        """
        return str(self.amount_range_id)


class LvrRange(BaseModel):
    lvr_range_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    min_lvr = models.IntegerField()
    max_lvr = models.IntegerField()

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"lvr_range'
        unique_together = ("loan_id", "min_lvr", "max_lvr")

    def __str__(self):
        """
        :return: Returns lvr_range_id
        """
        return str(self.lvr_range_id)


class ApplicableProperty(BaseModel):
    applies_to_property_type_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    property_type = models.CharField(max_length=75)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"applies_to_property_type'
        unique_together = ("loan_id", "property_type")

    def __str__(self):
        """
        :return: Returns applicable property id
        """
        return str(self.applies_to_property_type_id)


class ApplicableReason(BaseModel):
    applies_to_reason_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    reason = models.CharField(max_length=75)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"applies_to_reason'
        unique_together = ("loan_id", "reason")

    def __str__(self):
        """
        :return: Returns applicable reason id
        """
        return str(self.applies_to_reason_id)


class ApplicableState(BaseModel):
    applies_to_state_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    state = models.CharField(max_length=75)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"applies_to_state'
        unique_together = ("loan_id", "state")

    def __str__(self):
        """
        :return: Returns applicable state
        """
        return str(self.applies_to_state_id)


class Discount(BaseModel):
    discount_id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id')
    lvr_range_id = models.ForeignKey(LvrRange, on_delete=models.CASCADE, db_column='lvr_range_id')
    amount_range_id = models.ForeignKey(AmountRange, on_delete=models.CASCADE, db_column='amount_range_id')
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"discount'
        unique_together = ("loan_id", "lvr_range_id", "amount_range_id")

    def __str__(self):
        """
        :return: Returns discount id
        """
        return str(self.discount_id)


class Request(BaseModel):
    request_id = models.AutoField(primary_key=True)
    channel_path = models.CharField(max_length=75)
    partner_path = models.CharField(max_length=75, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    contact_time = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    amount = models.IntegerField()
    price = models.IntegerField()
    lvr = models.IntegerField()
    stamp_duty = models.IntegerField(blank=True, null=True)
    first_home_bg = models.IntegerField(blank=True, null=True)
    deposit = models.IntegerField(blank=True, null=True)
    new_property = models.NullBooleanField()
    current_repayment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    disposable_income = models.DecimalField(max_digits=8, decimal_places=2)
    show_fixed = models.BooleanField(default=True)
    show_variable = models.BooleanField(default=True)
    reason = models.CharField(max_length=50)
    property_type = models.CharField(max_length=50)
    trustee_is_a_company = models.NullBooleanField()
    trust_balance = models.IntegerField(blank=True, null=True)
    salescode = models.CharField(max_length=15, blank=True, null=True)
    kioskcode = models.CharField(max_length=15, blank=True, null=True)
    last_node = models.CharField(max_length=250, blank=True, null=True)
    ppr = models.NullBooleanField()
    discarded = models.BooleanField(default=False)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"request'

    def __str__(self):
        """
        :return: Return request_id
        """
        return str(self.request_id)


class RequestArchive(BaseModel):
    request_id = models.AutoField(primary_key=True)
    channel_path = models.CharField(max_length=75)
    partner_path = models.CharField(max_length=75, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    contact_time = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=75, blank=True, null=True)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    amount = models.IntegerField()
    price = models.IntegerField()
    lvr = models.IntegerField()
    stamp_duty = models.IntegerField(blank=True, null=True)
    first_home_bg = models.IntegerField(blank=True, null=True)
    deposit = models.IntegerField(blank=True, null=True)
    new_property = models.NullBooleanField()
    current_repayment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    disposable_income = models.DecimalField(max_digits=8, decimal_places=2)
    show_fixed = models.BooleanField(default=True)
    show_variable = models.BooleanField(default=True)
    reason = models.CharField(max_length=50)
    property_type = models.CharField(max_length=50)
    trustee_is_a_company = models.NullBooleanField()
    trust_balance = models.IntegerField(blank=True, null=True)
    salescode = models.CharField(max_length=15, blank=True, null=True)
    kioskcode = models.CharField(max_length=15, blank=True, null=True)
    last_node = models.CharField(max_length=250, blank=True, null=True)
    ppr = models.NullBooleanField()
    discarded = models.BooleanField(default=False)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"request_archive'

    def __str__(self):
        """
        :return: Return request_id in Request Archive
        """
        return str(self.request_id)


class RequestNote(BaseModel):
    note_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id')
    content = models.TextField()

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"request_note'

    def __str__(self):
        """
        :return: Returns request note id
        """
        return str(self.note_id)


class Quote(BaseModel):
    quote_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id', db_index=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, db_column='loan_id', db_index=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    cashback = models.IntegerField(blank=True, null=True)
    selected_on = models.DateTimeField(blank=True, null=True)
    p_and_i_estimate = models.IntegerField(blank=True, null=True)
    io_estimate = models.IntegerField(blank=True, null=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"quote'

    def __str__(self):
        """
        :return: Returns quote_id
        """
        return str(self.quote_id)


class RequestCookieMap(BaseModel):
    rc_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, db_column='request_id', db_index=True)
    cookie = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label = "home_loans"
        db_table = 'home_loans\".\"request_cookie'

    def __str__(self):
        """
        :return:
        """
        return str(self.rc_id)
