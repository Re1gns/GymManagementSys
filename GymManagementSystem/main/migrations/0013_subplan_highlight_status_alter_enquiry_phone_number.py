# Generated by Django 4.2.7 on 2023-12-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_subplan_alter_enquiry_phone_number_subplanfeature'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='highlight_status',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]