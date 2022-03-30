# Generated by Django 3.1.2 on 2022-03-26 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('catalog', '0002_auto_20220323_0208'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscriptionList',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('stock_list', models.ManyToManyField(to='catalog.Stock')),
            ],
        ),
    ]
