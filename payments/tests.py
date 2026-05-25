from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from accounts.models import Address
from catalog.models import Item
from orders.models import Order, OrderItem
from payments.gateways import (
    PaymentGatewayFactory,
    PayPalGateway,
    StripeGateway,
    StripeWalletGateway,
)
from payments.models import Payment
from payments.services import PaymentService


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="payuser", password="password")

    def test_payment_method_choices(self):
        for method, _ in Payment.METHOD_CHOICES:
            payment = Payment.objects.create(method=method, user=self.user, amount=10.00)
            self.assertEqual(payment.method, method)
            payment.delete()

    def test_payment_str(self):
        payment = Payment.objects.create(method='paypal', user=self.user, amount=25.00)
        self.assertIn('paypal', str(payment))
        self.assertIn('25.0', str(payment))


class PaymentGatewayFactoryTest(TestCase):
    def test_get_stripe_gateway(self):
        self.assertIsInstance(PaymentGatewayFactory.get_gateway('stripe'), StripeGateway)

    def test_get_paypal_gateway(self):
        self.assertIsInstance(PaymentGatewayFactory.get_gateway('paypal'), PayPalGateway)

    def test_get_apple_pay_gateway(self):
        self.assertIsInstance(PaymentGatewayFactory.get_gateway('apple_pay'), StripeWalletGateway)

    def test_get_google_pay_gateway(self):
        self.assertIsInstance(PaymentGatewayFactory.get_gateway('google_pay'), StripeWalletGateway)

    def test_unsupported_method_returns_none(self):
        self.assertIsNone(PaymentGatewayFactory.get_gateway('bitcoin'))

    def test_each_call_returns_fresh_instance(self):
        g1 = PaymentGatewayFactory.get_gateway('stripe')
        g2 = PaymentGatewayFactory.get_gateway('stripe')
        self.assertIsNot(g1, g2)


class StripeGatewayTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="stripeuser", password="password")
        self.address = Address.objects.create(
            user=self.user, street_address="1 Main St", apartment_address="",
            country="US", zip="10001", address_type="B",
        )
        self.item = Item.objects.create(
            title="Test", price=20.00, slug="test-item", description="Test",
        )

    @patch('stripe.Charge.create')
    @patch('stripe.Customer.create')
    def test_stripe_charge_success(self, mock_customer_create, mock_charge):
        mock_customer = MagicMock()
        mock_customer.__getitem__ = lambda self, key: 'cus_123' if key == 'id' else None
        mock_customer_create.return_value = mock_customer
        mock_charge.return_value = {'id': 'ch_123'}

        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        order_item = OrderItem.objects.create(user=self.user, item=self.item, quantity=1)
        order.items.add(order_item)

        gateway = StripeGateway()
        payment, error = gateway.create_charge(
            user=self.user, order=order,
            billing_address=self.address, shipping_address=self.address,
            token='tok_visa',
        )
        self.assertIsNone(error)
        self.assertIsNotNone(payment)
        self.assertEqual(payment.method, 'stripe')

    def test_stripe_charge_missing_token(self):
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        gateway = StripeGateway()
        payment, error = gateway.create_charge(
            user=self.user, order=order,
            billing_address=self.address, shipping_address=self.address,
        )
        self.assertIsNone(payment)
        self.assertIn('stripeToken', error)


class PayPalGatewayTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="paypaluser", password="password")
        self.address = Address.objects.create(
            user=self.user, street_address="2 Main St", apartment_address="",
            country="US", zip="10002", address_type="S",
        )

    def test_paypal_charge_missing_params(self):
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        gateway = PayPalGateway()
        payment, error = gateway.create_charge(
            user=self.user, order=order,
            billing_address=self.address, shipping_address=self.address,
        )
        self.assertIsNone(payment)
        self.assertIn('paypal_payment_id', error)

    def test_unsupported_method_in_service(self):
        order = Order.objects.create(user=self.user, ordered_date=timezone.now())
        payment, error = PaymentService.process_payment(
            user=self.user, order=order, method='bitcoin',
            billing_address_id=self.address.id,
            shipping_address_id=self.address.id,
        )
        self.assertIsNone(payment)
        self.assertIn('Unsupported', error)
