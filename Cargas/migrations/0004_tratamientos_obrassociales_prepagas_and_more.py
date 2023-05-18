# Generated by Django 4.2 on 2023-05-17 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cargas', '0003_tratamientos_código_interno_alter_tratamientos_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tratamientos_ObrasSociales_Prepagas',
            fields=[
                ('Obra_Social_Prepaga', models.CharField(max_length=40)),
                ('Tratamiento', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Código', models.IntegerField(null=True)),
                ('Precio', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Tratamientos Obras Sociales y Prepagas',
                'ordering': ['Tratamiento'],
            },
        ),
        migrations.CreateModel(
            name='Tratamientos_Propios',
            fields=[
                ('Código_interno', models.IntegerField(default=0)),
                ('Tratamiento', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Tratamientos Propios',
                'ordering': ['Tratamiento'],
            },
        ),
        migrations.RemoveField(
            model_name='tratamientos',
            name='Obra_social_prepaga',
        ),
        migrations.AlterField(
            model_name='presupuestos',
            name='Tratamiento_1',
            field=models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100),
        ),
        migrations.AlterField(
            model_name='presupuestos',
            name='Tratamiento_2',
            field=models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100),
        ),
        migrations.AlterField(
            model_name='presupuestos',
            name='Tratamiento_3',
            field=models.CharField(blank=True, choices=[('Muelas', 'Muelas'), ('Encías', 'Encías'), ('Implante', 'Implante')], max_length=100),
        ),
        migrations.DeleteModel(
            name='Obras_Sociales_Prepagas',
        ),
        migrations.DeleteModel(
            name='Tratamientos',
        ),
    ]