# Generated by Django 4.2.7 on 2023-12-08 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_subplan_max_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_month', models.IntegerField()),
                ('total_discount', models.IntegerField()),
                ('subplan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subplan')),
            ],
        ),
    ]
