# Generated by Django 4.2.7 on 2023-12-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_subscription_sub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banners',
            options={'verbose_name_plural': 'Banners'},
        ),
        migrations.AlterModelOptions(
            name='enquiry',
            options={'verbose_name_plural': 'Enquiries'},
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name_plural': 'Galleries'},
        ),
        migrations.AlterModelOptions(
            name='notifuserstatus',
            options={'verbose_name_plural': 'Notification Status'},
        ),
        migrations.AddField(
            model_name='trainer',
            name='facebook',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='instagram',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='twitter',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='youtube',
            field=models.URLField(null=True),
        ),
    ]
