# Generated by Django 4.2 on 2023-04-22 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cargas', '0003_rename_paciente_presupuestos_paciente_dni'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pacientes',
            options={'ordering': ['Nombre'], 'verbose_name_plural': 'Pacientes'},
        ),
        migrations.AlterModelOptions(
            name='presupuestos',
            options={'ordering': ['Número_de_orden'], 'verbose_name_plural': 'Presupuestos'},
        ),
    ]
