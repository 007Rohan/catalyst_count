# Generated by Django 5.1.1 on 2024-09-18 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_company_year_founded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='size_range',
            field=models.CharField(max_length=20),
        ),
    ]
