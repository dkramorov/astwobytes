# Generated by Django 2.2.3 on 2020-08-02 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weld', '0020_auto_20200801_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weldingjoint',
            name='titul',
        ),
        migrations.AddField(
            model_name='weldingjoint',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Заявку принял'),
        ),
        migrations.AddField(
            model_name='weldingjoint',
            name='requester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requester', to=settings.AUTH_USER_MODEL, verbose_name='Заявку подал'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='control_result',
            field=models.IntegerField(blank=True, choices=[(1, 'Вырез'), (2, 'Годен'), (3, 'Ремонт'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Результат контроля, например, Вырезать'),
        ),
    ]