# Generated by Django 4.2 on 2023-05-26 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobranzas',
            fields=[
                ('Número_de_comprobante', models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False)),
                ('Fecha_de_cobro', models.DateField(auto_now_add=True)),
                ('Cuánto_pagó', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Cobranzas',
                'ordering': ['Número_de_comprobante'],
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('Nombre', models.CharField(max_length=40)),
                ('DNI', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('Teléfono', models.IntegerField()),
                ('E_mail', models.CharField(max_length=40)),
                ('Obra_Social_Prepaga', models.CharField(max_length=40)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pacientes',
                'ordering': ['Nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tratamientos_Propios',
            fields=[
                ('Código_interno', models.IntegerField(default=0)),
                ('Tratamiento', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tratamientos Propios',
                'ordering': ['Código_interno'],
            },
        ),
        migrations.CreateModel(
            name='Tratamientos_ObrasSociales_Prepagas',
            fields=[
                ('Obra_Social_Prepaga', models.CharField(max_length=40)),
                ('Tratamiento', models.CharField(max_length=50)),
                ('Código', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('Precio', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tratamientos Obras Sociales y Prepagas',
                'ordering': ['Tratamiento'],
            },
        ),
        migrations.CreateModel(
            name='Presupuestos',
            fields=[
                ('Número_de_orden', models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False)),
                ('Fecha', models.DateField(auto_now_add=True)),
                ('Tratamiento_1', models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100)),
                ('Tratamiento_2', models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100)),
                ('Tratamiento_3', models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100)),
                ('Monto', models.IntegerField()),
                ('Paciente_Dni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Presupuestos', to='Cargas.pacientes')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Presupuestos',
                'ordering': ['Número_de_orden'],
            },
        ),
        migrations.CreateModel(
            name='CobranzasPresupuestos_Inter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cobranzas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cargas.cobranzas')),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cargas.presupuestos')),
            ],
        ),
        migrations.AddField(
            model_name='cobranzas',
            name='Número_de_orden',
            field=models.ManyToManyField(auto_created=True, related_name='Cobranzas', through='Cargas.CobranzasPresupuestos_Inter', to='Cargas.presupuestos'),
        ),
        migrations.AddField(
            model_name='cobranzas',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
