# Generated by Django 3.0.3 on 2020-05-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0014_auto_20200520_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(default='', null=True, upload_to='MisCosas'),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(default='', max_length=64),
        ),
    ]
