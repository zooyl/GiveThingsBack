# Generated by Django 2.1.7 on 2019-03-27 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_foundation_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteuser',
            name='gathering',
        ),
        migrations.AddField(
            model_name='gathering',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.SiteUser'),
            preserve_default=False,
        ),
    ]
