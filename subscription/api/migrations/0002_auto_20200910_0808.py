# Generated by Django 3.1.1 on 2020-09-10 08:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='editor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='journals', to='api.editor'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2021, 9, 10, 8, 8, 3, 882472)),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('journal', 'customer')},
        ),
    ]