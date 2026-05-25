from rest_framework import serializers
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'method', 'method_display', 'amount', 'timestamp')
        read_only_fields = ('id', 'timestamp')
