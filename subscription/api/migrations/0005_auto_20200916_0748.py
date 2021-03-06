# Generated by Django 3.1.1 on 2020-09-16 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200910_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='subscription_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editor',
            name='journals_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(default='2021-09-16'),
        ),
    ]
