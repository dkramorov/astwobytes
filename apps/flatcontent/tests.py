from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks

class FlatCatTests(TestCase):
    """Тестирование каталога
    """
    def test_cat_links(self):
        """Тестирование ссылок внутри
        """

        # Стандартный каталог
        catalogue = Containers.objects.create(name='test container', state=7, tag=settings.DEFAULT_CATALOGUE_TAG)
        block = Blocks.objects.create(name='cat1', container=catalogue, state=4)
        self.assertEqual('/cat/cat1/', block.link)

        # Альтернативные каталоги
        catalogue2 = Containers.objects.create(name='test container', state=7, tag='store')
        block = Blocks.objects.create(name='cat1', container=catalogue2, state=4)
        self.assertEqual('/cat/store/cat1/', block.link)

        # Ссыль на рубрику не меняется при сохранении
        catalogue2.tag = 'store2'
        catalogue2.save()
        block.create_cat_link()
        block.save()
        self.assertEqual('/cat/store/cat1/', block.link)

        # Ссыль на рубрику меняется, если сказать, что надо менять
        block.create_cat_link(force=True)
        block.save()
        self.assertEqual('/cat/store2/cat1/', block.link)
