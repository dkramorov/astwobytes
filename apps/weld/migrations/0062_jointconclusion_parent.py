# Generated by Django 2.2.3 on 2020-09-01 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0061_auto_20200901_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointconclusion',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.JointConclusion', verbose_name='При ремонте welding_joint пустой из-за связи, но ссылка на основное заключение должна быть, а также номер ремонта'),
        ),
    ]
