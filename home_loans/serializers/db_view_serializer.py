from rest_framework import serializers
from home_loans.models import PriceRequestView, PriceSMSFRequestView, QuotesView


class PriceRequestViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceRequestView
        fields = '__all__'


class PriceSMSFRequestViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceSMSFRequestView
        fields = '__all__'


class QuotesViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuotesView
        fields = '__all__'
