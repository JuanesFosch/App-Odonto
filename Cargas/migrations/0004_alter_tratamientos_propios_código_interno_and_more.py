# Generated by Django 4.2 on 2023-06-02 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cargas', '0003_alter_tratamientos_propios_código_interno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamientos_propios',
            name='Código_interno',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tratamientos_propios',
            name='Tratamiento',
            field=models.CharField(max_length=50),
        ),
    ]
