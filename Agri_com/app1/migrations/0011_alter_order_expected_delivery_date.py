# Generated by Django 5.1.7 on 2025-04-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expected_delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
