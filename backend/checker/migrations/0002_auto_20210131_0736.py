# Generated by Django 3.1.5 on 2021-01-30 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptomsmodel',
            name='ID',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]