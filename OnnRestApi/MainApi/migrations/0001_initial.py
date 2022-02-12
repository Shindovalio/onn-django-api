# Generated by Django 3.2.4 on 2022-02-12 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('stock', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=300)),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='MainApi.product')),
            ],
        ),
    ]
