# Generated by Django 2.2.3 on 2020-08-09 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weld', '0028_auto_20200809_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeldingJointState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Время смены статуса')),
                ('from_state', models.IntegerField(blank=True, choices=[(1, 'Новый стык'), (2, 'В работе'), (3, 'Готовый стык'), (4, 'В ремонте')], db_index=True, null=True, verbose_name='Статус заявки, например, в работе')),
                ('to_state', models.IntegerField(blank=True, choices=[(1, 'Новый стык'), (2, 'В работе'), (3, 'Готовый стык'), (4, 'В ремонте')], db_index=True, null=True, verbose_name='Статус заявки, например, в работе')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, сменивший статус')),
                ('welding_joint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.WeldingJoint', verbose_name='Заявка на стык')),
            ],
            options={
                'verbose_name': 'Сварочные соединения - Смена статуса заявки на стык',
                'verbose_name_plural': 'Сварочные соединения - Смена статусов заявкок на стыки',
            },
        ),
    ]
