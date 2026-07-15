from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_add_usdc_payment_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='category',
            field=models.CharField(
                choices=[
                    ('stock', 'Stock'),
                    ('crypto', 'Crypto'),
                    ('etf', 'ETF'),
                    ('indices', 'Indices'),
                    ('forex', 'Forex'),
                ],
                default='stock',
                max_length=20,
            ),
        ),
    ]
