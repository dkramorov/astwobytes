# -*- coding: utf-8 -*-
#from djapian import space, Indexer, CompositeIndexer
from djapian.forindex import space, NewIndexer
from apps.flatcontent.models import Containers, Blocks

class ContainersIndexer(NewIndexer):
    fields = ('name',)
    tags = [
      ('tag', 'tag'),
    ]
space.add_index(Containers, ContainersIndexer, attach_as='indexer')

class BlocksIndexer(NewIndexer):
    fields = (
        ('name', 10),
        #'get_body',
        ('tag', 10),
        ('title', 4),
        ('description', 4),
        ('keywords', 4),
    )
  #tags = [
    #('name', 'name', 2),
    #('body', 'body'),
  #]
space.add_index(Blocks, BlocksIndexer, attach_as='indexer')
