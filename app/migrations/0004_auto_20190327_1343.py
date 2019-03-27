# Generated by Django 2.1.7 on 2019-03-27 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20190322_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foundation',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category'),
        ),
        migrations.AlterField(
            model_name='gathering',
            name='needed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category'),
        ),
        migrations.AlterField(
            model_name='giveaway',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category'),
        ),
        migrations.AlterField(
            model_name='giveaway',
            name='foundation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Foundation'),
        ),
    ]
