# Generated by Django 4.2.16 on 2024-11-25 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_orderitem_total_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-order_date']},
        ),
    ]
