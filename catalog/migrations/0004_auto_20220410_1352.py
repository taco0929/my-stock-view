# Generated by Django 3.1.2 on 2022-04-10 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20220405_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyprice',
            name='date_time',
            field=models.DateTimeField(db_index=True, help_text='default timezone:UTF'),
        ),
    ]
