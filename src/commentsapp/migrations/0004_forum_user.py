# Generated by Django 3.0.8 on 2020-09-07 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commentsapp', '0003_auto_20200907_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commentsapp.profile'),
        ),
    ]
