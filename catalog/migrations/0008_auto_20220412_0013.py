# Generated by Django 3.1.2 on 2022-04-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20220410_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlineid',
            name='token',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='userlineid',
            name='token_ini',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userlineid',
            name='line_id',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
