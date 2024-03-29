# Generated by Django 3.2.6 on 2021-08-13 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=None, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ready_status',
            field=models.CharField(default='sold', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='order',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='order',
            name='source',
            field=models.CharField(default='cash-register', max_length=10),
        ),
    ]
