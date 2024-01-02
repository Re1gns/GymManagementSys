# Generated by Django 4.2.7 on 2024-01-01 08:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_appsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='details',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='details',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_detail',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='page',
            name='detail',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='details',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='details',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trainermsg',
            name='message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trainernotification',
            name='notif_msg',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trainersachievements',
            name='details',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trainersubscriberreport',
            name='report_msg',
            field=ckeditor.fields.RichTextField(),
        ),
    ]