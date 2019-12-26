# -*- coding:utf-8 -*-
from django.db import models

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard

class ConversationGroup(Standard):
    """Группы для бесед, когда в беседе участвуют
       больше чем 2 человека, в список контактов
       не добавляем групповые беседы"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    user_id = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Пользователь, который создал беседу')

    class Meta:
        verbose_name = 'Чат - Группы'
        verbose_name_plural = 'Чат - Группы'

class Messages(Standard):
    """Сообщения для чата
       state = (None => непрочитано, 1 => прочитано)"""
    from_user = models.IntegerField(blank=True, null=True, db_index=True)
    to_user = models.IntegerField(blank=True, null=True, db_index=True)
    text = models.TextField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(ConversationGroup, blank=True, null=True, on_delete=models.CASCADE)
    # Группа содержит from_user + group_id, to_user = NULL,
    # так мы сможем выбирать отдельно личные сообщения, а отдельно для группы

    class Meta:
        verbose_name = 'Чат - Сообщения'
        verbose_name_plural = 'Чат - Сообщения'

class BcastMessages(Standard):
    """Широковещательные сообщения для всех"""
    from_user = models.IntegerField(blank=True, null=True, db_index=True)
    text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Чат - Широковещательные сообщения'
        verbose_name_plural = 'Чат - Широковещательные сообщения'

class Conversations(Standard):
    """Контактов может быть достаточно много,
       но вот чтобы показывать кол-во новых
       сообщений и с кем были беседы,
       необходим список для пользователя по беседам"""
    user_id = models.IntegerField(blank=True, null=True, db_index=True)
    contact = models.IntegerField(blank=True, null=True, db_index=True)
    group = models.ForeignKey(ConversationGroup, blank=True, null=True, on_delete=models.CASCADE)
    # Группа содержит user_id + group_id, contact = NULL,
    # так мы сможем выбирать отдельно контакты, а отдельно группы

    # Мы должны отпрвлять сообщение всем пользователям в группе,
    # но помечать, что сообщение отправляется для группы,
    # не кокретно пользователю а группе пользователей

    # У бесед у нас как раз ответ по айдишникам

    class Meta:
        verbose_name = 'Чат - Беседы'
        verbose_name_plural = 'Чат - Беседы'

