# Generated by Django 4.1 on 2022-08-12 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Item')),
                ('pontos', models.PositiveIntegerField(verbose_name='Pontos')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sobrevivente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('idade', models.PositiveIntegerField(verbose_name='Idade')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('infectado', models.BooleanField(default=False, verbose_name='Infectado?')),
            ],
            options={
                'verbose_name': 'Sobrevivente',
                'verbose_name_plural': 'Sobreviventes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geral.item', verbose_name='Item')),
                ('sobrevivente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geral.sobrevivente', verbose_name='Sobrevivente')),
            ],
            options={
                'verbose_name': 'Inventário',
                'verbose_name_plural': 'Inventários',
                'ordering': ['id'],
            },
        ),
    ]
