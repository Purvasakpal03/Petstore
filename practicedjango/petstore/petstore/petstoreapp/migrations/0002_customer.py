# Generated by Django 5.0.6 on 2024-05-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petstoreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phoneno', models.BigIntegerField()),
                ('password', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
    ]
