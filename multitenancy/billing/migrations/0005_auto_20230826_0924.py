# Generated by Django 3.2.12 on 2023-08-26 07:24

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multitenancy.billing.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0015_alter_plan_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0004_auto_20230825_0201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='The currency code.', max_length=3, unique=True)),
                ('name', models.CharField(help_text='The name of the currency.', max_length=50)),
                ('exchange_rate', models.DecimalField(decimal_places=4, help_text='The exchange rate of the currency.', max_digits=10)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='The date and time the payment was created.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='details',
            field=models.TextField(blank=True, help_text='Additional details about the payment.', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='failed_reason',
            field=models.TextField(blank=True, help_text='The reason for a failed payment.', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='The ID of the payment transaction.', unique=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time the payment was last updated.'),
        ),
        migrations.AddField(
            model_name='refund',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='credit',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='credit',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(upload_to=multitenancy.billing.models.invoice_directory_path),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='subscriptions.subscription'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='The amount of the payment.', max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='gateway',
            field=models.ForeignKey(help_text='The payment gateway used for the payment.', on_delete=django.db.models.deletion.PROTECT, to='billing.paymentgateway'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], db_index=True, help_text='The status of the payment.', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='subscriber',
            field=models.ForeignKey(help_text='The user who made the payment.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='refund',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='billing.invoice'),
        ),
        migrations.AlterField(
            model_name='refund',
            name='reason',
            field=models.CharField(max_length=255),
        ),
        migrations.AddIndex(
            model_name='credit',
            index=models.Index(fields=['customer'], name='billing_cre_custome_53b135_idx'),
        ),
        migrations.AddConstraint(
            model_name='credit',
            constraint=models.UniqueConstraint(fields=('customer',), name='unique_customer_credit'),
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.ForeignKey(help_text='The currency used for the payment.', null=True, on_delete=django.db.models.deletion.PROTECT, to='billing.currency'),
        ),
    ]
