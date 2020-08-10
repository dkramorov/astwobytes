# Generated by Django 2.2.3 on 2020-07-15 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0002_auto_20200714_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Свариваемый элемент',
                'verbose_name_plural': 'Свариваемые элементы',
            },
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='join_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weld.JoinType', verbose_name='Свариваемые элементы, например, тройник/переходник'),
        ),
    ]