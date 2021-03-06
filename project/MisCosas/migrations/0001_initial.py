# Generated by Django 3.0.3 on 2020-05-06 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alimentador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alimentadorId', models.CharField(default='', max_length=64)),
                ('nombre', models.CharField(max_length=64)),
                ('enlace', models.CharField(max_length=64)),
                ('type', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('enlace', models.CharField(max_length=64)),
                ('itemId', models.CharField(default='', max_length=64)),
                ('fotoVideo', models.CharField(default='', max_length=64)),
                ('descripcion', models.TextField(default='')),
                ('votosPositivos', models.IntegerField(default=0)),
                ('votosNegativos', models.IntegerField(default=0)),
                ('usuario', models.CharField(default='', max_length=64)),
                ('alimentador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MisCosas.Alimentador')),
            ],
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(default='', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('email', models.EmailField(default='', max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('itemsvotados', models.ManyToManyField(to='MisCosas.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='estadoVoto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MisCosas.Voto'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(default='', max_length=64)),
                ('fecha', models.DateTimeField(verbose_name='publicado')),
                ('cuerpo', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MisCosas.Item')),
            ],
        ),
    ]
