# Generated by Django 3.0.3 on 2020-05-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0009_auto_20200510_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='image',
            field=models.ImageField(default=None, upload_to='MisCosas/static/MisCosas'),
            preserve_default=False,
        ),
    ]
