# Generated by Django 4.2.7 on 2023-11-30 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_gallery_galleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='Gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.gallery'),
        ),
    ]