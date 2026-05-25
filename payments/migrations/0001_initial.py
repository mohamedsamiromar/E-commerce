import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(blank=True, max_length=50, null=True)),
                ('paypal_payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('method', models.CharField(
                    choices=[
                        ('stripe', 'Stripe'), ('paypal', 'PayPal'),
                        ('apple_pay', 'Apple Pay'), ('google_pay', 'Google Pay'),
                    ],
                    default='stripe', max_length=10,
                )),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
    ]
