# Generated by Django 5.1.1 on 2024-09-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_year_founded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='year_founded',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
