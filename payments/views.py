from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from payments.gateways import PaymentGatewayFactory
from payments.services import PaymentService


class PaymentView(APIView):
    def post(self, request):
        order = Order.objects.filter(user=request.user, ordered=False).first()
        if not order:
            return Response(
                {"message": "You do not have an active order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        method = request.data.get('method', 'stripe')
        if method not in PaymentGatewayFactory.get_supported_methods():
            return Response(
                {"message": f"Unsupported payment method: {method}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = request.data
        if method == 'stripe' and not data.get('stripeToken'):
            return Response(
                {"message": "stripeToken is required for Stripe payments"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if method == 'paypal' and not (data.get('paypal_payment_id') and data.get('payer_id')):
            return Response(
                {"message": "paypal_payment_id and payer_id are required for PayPal"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if method in ('apple_pay', 'google_pay') and not data.get('payment_method_id'):
            return Response(
                {"message": "payment_method_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        payment, error = PaymentService.process_payment(
            user=request.user,
            order=order,
            method=method,
            token=data.get('stripeToken'),
            payment_method_id=data.get('payment_method_id'),
            paypal_payment_id=data.get('paypal_payment_id'),
            payer_id=data.get('payer_id'),
            billing_address_id=data.get('billing_address_id') or data.get('selectedBillingAddress'),
            shipping_address_id=data.get('shipping_address_id') or data.get('selectedShippingAddress'),
        )
        if error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Payment successful", "payment_id": payment.id},
            status=status.HTTP_200_OK,
        )
