# Generated by Django 2.2.3 on 2020-07-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0011_auto_20200725_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='contractor',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Наименоваение генподрядной и строительной организации и ее ведомственная принадлежность, например, АО "Хоневелл"'),
        ),
        migrations.AddField(
            model_name='company',
            name='fitter',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Наименование монтажной организации, например, ООО "Транспромстрой"'),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Место строительства предприятия, например, Ярактикинское НГКМ'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Компания, наименование предприятия-заказчика, например, ООО "ИНК"'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Наименование сооружаемого объекта, например, '),
        ),
    ]
