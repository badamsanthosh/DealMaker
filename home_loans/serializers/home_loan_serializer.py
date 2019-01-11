from rest_framework import serializers
from home_loans.models import Loan, Request, RequestArchive, Quote, AmountRange, LvrRange, Discount, RequestNote
from home_loans.models import ApplicableProperty, ApplicableReason, ApplicableState, RequestCookieMap


class LoanSerializer(serializers.ModelSerializer):

    frequencies = serializers.ListField(child=serializers.CharField(max_length=50))

    class Meta:
        model = Loan
        exclude = ('parent_id', )


class AmountRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AmountRange
        fields = '__all__'


class LvrRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LvrRange
        fields = '__all__'


class ApplicablePropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicableProperty
        exclude = ('applies_to_property_type_id', )


class ApplicableReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicableReason
        exclude = ('applies_to_reason_id', )


class ApplicableStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicableState
        exclude = ('applies_to_state_id', )


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'


class RequestArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestArchive
        fields = '__all__'


class RequestNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestNote
        fields = '__all__'


class RequestCookieMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestCookieMap
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        exclude = ('created_on', 'updated_on', 'is_current', )

