from abc import ABC, abstractmethod

import paypalrestsdk
import stripe
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from accounts.models import UserProfile
from payments.models import Payment


class PaymentGateway(ABC):
    @abstractmethod
    def create_charge(self, user, order, billing_address, shipping_address, **kwargs):
        ...

    @abstractmethod
    def create_customer(self, user):
        ...


class StripeGateway(PaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.api = stripe

    def create_charge(self, user, order, billing_address, shipping_address, **kwargs):
        token = kwargs.get('token')
        if not token:
            return None, "stripeToken is required"
        try:
            userprofile, _ = UserProfile.objects.get_or_create(user=user)
            if userprofile.stripe_customer_id:
                customer = self.api.Customer.retrieve(userprofile.stripe_customer_id)
                customer.sources.create(source=token)
            else:
                customer = self.api.Customer.create(email=user.email)
                customer.sources.create(source=token)
                userprofile.stripe_customer_id = customer['id']
                userprofile.one_click_purchasing = True
                userprofile.save()
            charge = self.api.Charge.create(
                amount=int(order.get_total() * 100),
                currency="usd",
                customer=userprofile.stripe_customer_id,
            )
            return self._finalize_order(order, user, charge['id'], billing_address, shipping_address)
        except stripe.error.CardError as e:
            return None, e.json_body.get('error', {}).get('message', 'Card was declined')
        except stripe.error.RateLimitError:
            return None, "Too many requests. Please try again."
        except stripe.error.InvalidRequestError:
            return None, "Invalid payment parameters"
        except stripe.error.AuthenticationError:
            return None, "Payment authentication failed"
        except stripe.error.APIConnectionError:
            return None, "Network error. Please try again."
        except stripe.error.StripeError:
            return None, "Something went wrong. You were not charged."

    def create_customer(self, user):
        customer = self.api.Customer.create(email=user.email)
        UserProfile.objects.update_or_create(
            user=user, defaults={'stripe_customer_id': customer['id']}
        )
        return customer

    @staticmethod
    @transaction.atomic
    def _finalize_order(order, user, charge_id, billing_address, shipping_address):
        payment = Payment.objects.create(
            stripe_charge_id=charge_id,
            method='stripe',
            user=user,
            amount=order.get_total(),
        )
        order.items.filter(ordered=False).update(ordered=True)
        order.ordered = True
        order.payment = payment
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.ordered_date = timezone.now()
        order.save()
        return payment, None


class StripeWalletGateway(StripeGateway):
    """Handles Apple Pay and Google Pay via Stripe PaymentIntent."""

    def create_charge(self, user, order, billing_address, shipping_address, **kwargs):
        payment_method_id = kwargs.get('payment_method_id')
        if not payment_method_id:
            return None, "payment_method_id is required"
        try:
            intent = self.api.PaymentIntent.create(
                amount=int(order.get_total() * 100),
                currency="usd",
                payment_method=payment_method_id,
                confirmation_method="manual",
                confirm=True,
                off_session=True,
            )
            charge_id = intent['charges']['data'][0]['id']
            return self._finalize_order(order, user, charge_id, billing_address, shipping_address)
        except stripe.error.CardError as e:
            return None, e.json_body.get('error', {}).get('message', 'Card was declined')
        except stripe.error.StripeError as e:
            return None, str(e)


class PayPalGateway(PaymentGateway):
    def __init__(self):
        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET,
        })
        self.api = paypalrestsdk

    def create_charge(self, user, order, billing_address, shipping_address, **kwargs):
        payment_id = kwargs.get('paypal_payment_id')
        payer_id = kwargs.get('payer_id')
        if not payment_id or not payer_id:
            return None, "paypal_payment_id and payer_id are required"
        try:
            paypal_payment = self.api.Payment.find(payment_id)
            if not paypal_payment.execute({'payer_id': payer_id}):
                return None, paypal_payment.error or "PayPal payment execution failed"
            return self._finalize_order(
                order, user, paypal_payment['id'], billing_address, shipping_address
            )
        except Exception as e:
            return None, str(e)

    def create_customer(self, user):
        pass

    @staticmethod
    @transaction.atomic
    def _finalize_order(order, user, paypal_id, billing_address, shipping_address):
        payment = Payment.objects.create(
            paypal_payment_id=paypal_id,
            method='paypal',
            user=user,
            amount=order.get_total(),
        )
        order.items.filter(ordered=False).update(ordered=True)
        order.ordered = True
        order.payment = payment
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.ordered_date = timezone.now()
        order.save()
        return payment, None


class PaymentGatewayFactory:
    _registry = {
        'stripe': StripeGateway,
        'paypal': PayPalGateway,
        'apple_pay': StripeWalletGateway,
        'google_pay': StripeWalletGateway,
    }

    @classmethod
    def get_gateway(cls, method):
        gateway_class = cls._registry.get(method)
        if gateway_class is None:
            return None
        return gateway_class()

    @classmethod
    def get_supported_methods(cls):
        return list(cls._registry.keys())
