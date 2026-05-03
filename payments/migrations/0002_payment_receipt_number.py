from django.db import migrations, models


def backfill_receipt_numbers(apps, schema_editor):
    Payment = apps.get_model('payments', 'Payment')
    for payment in Payment.objects.order_by('id'):
        payment.receipt_number = f'RCP-{payment.id:05d}'
        payment.save(update_fields=['receipt_number'])


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        # Step 1: Add field WITHOUT unique constraint first
        migrations.AddField(
            model_name='payment',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=20, default=''),
            preserve_default=False,
        ),
        # Step 2: Backfill all existing rows with real unique receipt numbers
        migrations.RunPython(backfill_receipt_numbers, reverse_code=migrations.RunPython.noop),
        # Step 3: Now safely apply the unique constraint
        migrations.AlterField(
            model_name='payment',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
