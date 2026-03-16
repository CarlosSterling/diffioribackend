from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderitem_product_orderitem_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='wompi_transaction_id',
            field=models.CharField(blank=True, help_text='ID de transacción en Wompi', max_length=255, null=True),
        ),
    ]
