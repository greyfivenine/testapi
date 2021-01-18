from rest_framework import serializers

from .models import Customer, Deal, Item


class CustInfoSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField(source='deals_sum')
    username = serializers.CharField(max_length=128, source='customer__name')
    gems = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ("username", "spent_money", "gems")

    def get_gems(self, obj):
        return [elem for elem in obj['gems'] if elem]


class DealCreateSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(max_length=128)
    item = serializers.CharField(max_length=128)
    date = serializers.DateTimeField()

    class Meta:
        model = Deal
        fields = '__all__'

    def create(self, validated_data):
        customer_obj = Customer.objects.get_or_create(name=validated_data['customer'])[0]
        item_obj = Item.objects.get_or_create(name=validated_data['item'])[0]
        return Deal.objects.get_or_create(customer=customer_obj,
                                          item=item_obj,
                                          total=validated_data['total'],
                                          quantity=validated_data['quantity'],
                                          date=validated_data['date'])[0]
