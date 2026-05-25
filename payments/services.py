from accounts.models import Address
from payments.gateways import PaymentGatewayFactory


class PaymentService:
    @staticmethod
    def process_payment(user, order, method, **kwargs):
        gateway = PaymentGatewayFactory.get_gateway(method)
        if not gateway:
            return None, f"Unsupported payment method: {method}"
        billing_address = Address.objects.filter(
            id=kwargs.get('billing_address_id'), user=user
        ).first()
        shipping_address = Address.objects.filter(
            id=kwargs.get('shipping_address_id'), user=user
        ).first()
        if not billing_address or not shipping_address:
            return None, "Invalid billing or shipping address"
        return gateway.create_charge(
            user=user,
            order=order,
            billing_address=billing_address,
            shipping_address=shipping_address,
            **kwargs,
        )
