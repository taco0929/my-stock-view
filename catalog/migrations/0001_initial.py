# Generated by Django 3.1.2 on 2022-04-05 09:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('name', models.CharField(help_text='Enter the name of the sector', max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('name', models.CharField(help_text='Enter name of the stock', max_length=20)),
                ('code', models.CharField(help_text='Enter code of the stock', max_length=10, primary_key=True, serialize=False)),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.sector')),
            ],
        ),
        migrations.CreateModel(
            name='StockInformation',
            fields=[
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.stock')),
                ('business_describ', models.TextField(blank=True, help_text='Enter the describtion of the corps.', null=True)),
                ('market_value', models.IntegerField(blank=True, help_text='Enter the market value of the corps', null=True)),
                ('roe', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('roa', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('revenue', models.IntegerField(blank=True, max_length=20, null=True)),
                ('revenue_growth', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('revenue_per_share', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubList',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('stock_list', models.ManyToManyField(blank=True, null=True, to='catalog.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of the news', max_length=100)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, help_text='Enter the content of the news', null=True)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('related_stock', models.ManyToManyField(blank=True, null=True, to='catalog.Stock')),
            ],
            options={
                'ordering': ['-date_time'],
            },
        ),
        migrations.CreateModel(
            name='HistoryPriceSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('high', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('low', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('open', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('close', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('change', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('change_p', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.stock')),
            ],
            options={
                'ordering': ['stock', '-date'],
            },
        ),
        migrations.CreateModel(
            name='HistoryPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(db_index=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.stock')),
            ],
            options={
                'ordering': ['stock_code', 'date_time'],
            },
        ),
    ]
