# Generated by Django 2.2.3 on 2020-01-19 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeswitch', '0003_auto_20200119_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='CdrCsv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${caller_id_name}", "jocker"')),
                ('cid_name', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${caller_id_number}", "jocker"')),
                ('dest', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${destination_number}", "021067405"')),
                ('context', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${context}", "rtmp_context"')),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='"${start_stamp}", "2015-08-07 22:36:38"')),
                ('answered', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='"${answer_stamp}", "2015-08-07 22:36:40"')),
                ('ended', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='"${end_stamp}", "2015-08-07 22:36:44"')),
                ('duration', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='"${duration}", "6"')),
                ('billing', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='"${billsec}", "4"')),
                ('state', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${hangup_cause}", "NORMAL_CLEARING"')),
                ('uuid', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${uuid}", "b01e66de-8997-4e33-9907-4a237b22e049"')),
                ('bleg_uuid', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${bleg_uuid}", "cb2c6082-2519-472d-8748-6d310b01d992"')),
                ('account', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${accountcode}", "jocker"')),
                ('read_codec', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${read_codec}", "GSM"')),
                ('write_codec', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='"${write_codec}", "GSM"')),
                ('ip', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Айпи адрес')),
                ('user_agent', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='С какого приложения звонок')),
                ('client_id', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Ид компании, телефон которой в dest')),
                ('client_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название компании, телефон которой в dest')),
                ('personal_user_id', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Ид пользователя на сайте')),
                ('personal_user_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя пользователя на сайте')),
            ],
        ),
    ]