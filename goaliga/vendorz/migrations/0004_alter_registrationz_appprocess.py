# Generated by Django 4.1 on 2022-08-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorz', '0003_alter_registrationz_appprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationz',
            name='appProcess',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Under_Process ', 'Under_Process'), ('Rejected', 'Rejected'), ('Approved', 'Approved')], default='Applied', max_length=100, null=True),
        ),
    ]
