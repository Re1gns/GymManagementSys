# Generated by Django 4.2.7 on 2023-12-20 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_subplan_validity_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='sub_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
