# Generated by Django 4.1.1 on 2022-09-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_customer_email_alter_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(default='SITY', max_length=20),
            preserve_default=False,
        ),
    ]
