# Generated by Django 3.0.3 on 2020-05-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0011_remove_users_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='image',
            field=models.ImageField(null=True, upload_to='MisCosas'),
        ),
    ]
